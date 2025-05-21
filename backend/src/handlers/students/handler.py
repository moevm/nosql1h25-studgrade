from typing import Optional, List, Literal
from datetime import date
from fastapi import APIRouter, HTTPException, Query, status
from bson import ObjectId
from pydantic import TypeAdapter
from src.utils.security import generate_random_password, hash_password

from src.schemas.students import (
    Student,
    StudentWithStatistic,
    StudentBulkCreateResponse,
)
from src.db import db

router = APIRouter()


@router.get("/", response_model=List[StudentWithStatistic])
async def get_all_students(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    birth_date: Optional[str] = Query(None, examples={"date": {"summary": "YYYY-MM-DD"}}),
    admission_year: Optional[int] = Query(None, ge=1900, le=2100),
    student_type: Optional[List[Literal["bachelor", "master", "aspirant", "specialist"]]] = Query(None),
    course: Optional[int] = Query(None, ge=1),
    program_name: Optional[str] = Query(None),
    faculty: Optional[List[Literal["ФКТИ", "ФИБС", "ГФ"]]] = Query(None),
    group_name: Optional[List[Literal["2323", "1421", "3501"]]] = Query(None),
    limit: Optional[int] = Query(10, gt=0),
    offset: Optional[int] = Query(0, ge=0),
    sort_by: Optional[str] = Query("last_name"),
    order: Optional[Literal["asc", "desc"]] = Query("asc"),
):
    query = {}
    if first_name:
        query["firstName"] = {"$regex": first_name, "$options": "i"}

    if last_name:
        query["lastName"] = {"$regex": last_name, "$options": "i"}

    if birth_date:
        query["birthDate"] = birth_date

    if admission_year is not None:
        query["admissionYear"] = admission_year

    if student_type:
        query["studentType"] = {"$in": student_type}

    if course is not None:
        query["course"] = course
    if program_name:
        query["programName"] = program_name

    if faculty:
        query["faculty"] = {"$in": faculty}

    if group_name:
        query["groupName"] = {"$in": group_name}

    allowed_sort_fields = [
        "first_name",
        "last_name",
        "birth_date",
        "admission_year",
        "student_type",
        "course",
        "program_name",
        "faculty",
        "group_name",
    ]
    sort_field = sort_by if sort_by in allowed_sort_fields else "last_name"
    sort_order = 1 if order == "asc" else -1

    cursor = (
        db.students.find(query)
        .sort(sort_field, sort_order)
        .skip(offset)
        .limit(limit)
    )
    students = await cursor.to_list(length=None)
    for student in students:
        student["_id"] = str(student["_id"])

    adapter = TypeAdapter(List[StudentWithStatistic])
    return adapter.validate_python(students)


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    try:
        # 1) создаём связанного User
        user_id, raw_pwd = await _create_linked_user(student)

        # 2) сохраняем самого студента
        student_dict = student.model_dump(by_alias=True, exclude={"id", "user_id"})
        student_dict["userId"] = ObjectId(user_id)

        bd = student_dict.get("birthDate")
        if isinstance(bd, date):
            student_dict["birthDate"] = bd.isoformat()

        async with await db.client.start_session() as s:
            async with s.start_transaction():
                res = await db.students.insert_one(student_dict, session=s)

        created = await db.students.find_one({"_id": res.inserted_id})
        created["_id"] = str(created["_id"])
        created["rawPassword"] = raw_pwd  # ← покажем однократно
        created["userId"] = user_id
        return created

    except Exception as e:
        raise HTTPException(500, f"Database operation failed: {e}")


@router.get("/{student_id}", response_model=StudentWithStatistic)
async def get_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student["_id"] = str(student["_id"])
    return TypeAdapter(StudentWithStatistic).validate_python(student)


@router.patch("/{student_id}", response_model=StudentWithStatistic)
async def update_student(student_id: str, student: Student):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")

    existing = await db.students.find_one({"_id": ObjectId(student_id)})
    if not existing:
        raise HTTPException(404, "Student not found")

    update_data = student.model_dump(by_alias=True, exclude_unset=True)
    if "birthDate" in update_data and isinstance(update_data["birthDate"], date):
        update_data["birthDate"] = update_data["birthDate"].isoformat()

    async with await db.client.start_session() as s:
        async with s.start_transaction():
            if update_data:
                await db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data}, session=s)

            # ----- синхронизируем User -----
            user_updates = {}
            for field, alias in [("first_name", "firstName"), ("last_name", "lastName")]:
                if field in student.__fields_set__:
                    user_updates[alias] = getattr(student, field)

            if user_updates:
                await db.users.update_one({"_id": existing["userId"]}, {"$set": user_updates}, session=s)

    updated = await db.students.find_one({"_id": ObjectId(student_id)})
    updated["_id"] = str(updated["_id"])
    return TypeAdapter(StudentWithStatistic).validate_python(updated)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(400, "Invalid student ID")
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(404, "Student not found")

    async with await db.client.start_session() as s:
        async with s.start_transaction():
            await db.students.delete_one({"_id": ObjectId(student_id)}, session=s)
            await db.users.delete_one({"_id": student["userId"]}, session=s)


@router.post(
    "/bulk/",
    response_model=StudentBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["students", "bulk"],
)
async def bulk_create_students(students: List[Student]):
    try:
        students_dicts = []
        inserted_user_ids = []

        async with await db.client.start_session() as s:
            async with s.start_transaction():
                for st in students:
                    user_id, _ = await _create_linked_user(st)
                    inserted_user_ids.append(user_id)

                    sd = st.model_dump(by_alias=True, exclude={"id", "user_id"})
                    sd["userId"] = ObjectId(user_id)

                    if isinstance(sd["birthDate"], date):
                        sd["birthDate"] = sd["birthDate"].isoformat()

                    students_dicts.append(sd)

                result = await db.students.insert_many(students_dicts, session=s)

        return StudentBulkCreateResponse(inserted_ids=[str(i) for i in result.inserted_ids])

    except Exception as e:
        raise HTTPException(500, f"Bulk create failed: {e}")


def _generate_login(first_name: str, last_name: str) -> str:
    return f"{first_name[0].lower()}.{last_name.lower()}"


async def _create_linked_user(student: Student) -> tuple[str, str]:
    raw_pwd = generate_random_password()
    pwd_hash = hash_password(raw_pwd)

    login = _generate_login(student.first_name, student.last_name)
    email = f"{login}@example.com"

    user_dict = {
        "firstName": student.first_name,
        "middleName": None,
        "lastName": student.last_name,
        "login": login,
        "email": student,
        "passwordHash": pwd_hash,
        "role": "student",
    }
    result = await db.users.insert_one(user_dict)
    return str(result.inserted_id), raw_pwd
