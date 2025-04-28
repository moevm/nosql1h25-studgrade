from typing import Optional, List, Literal
from fastapi import APIRouter, HTTPException, Query, status
from datetime import datetime, date
from bson import ObjectId
from pydantic import TypeAdapter

from src.schemas.students import Student, StudentWithStatistic
from src.db import db


router = APIRouter()


@router.get("/", response_model=List[StudentWithStatistic])
async def get_all_students(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    birth_date: Optional[str] = Query(None, examples={"date": {"summary": "YYYY-MM-DD"}}),
    admission_year: Optional[int] = Query(None, ge=1900, le=2100),
    student_type: Optional[Literal["bachelor", "master", "aspirant", "specialist"]] = Query(None),
    course: Optional[int] = Query(None, ge=1),
    program_name: Optional[str] = Query(None),
    faculty: Optional[str] = Query(None),
    group_name: Optional[str] = Query(None),
    limit: Optional[int] = Query(10, gt=0),
    offset: Optional[int] = Query(0, ge=0),
    sort_by: Optional[str] = Query("last_name"),
    order: Optional[Literal["asc", "desc"]] = Query("asc"),
):

    query: dict = {}
    if first_name:
        query["first_name"] = {"$regex": first_name, "$options": "i"}
    if last_name:
        query["last_name"] = {"$regex": last_name, "$options": "i"}
    if birth_date:
        query["birth_date"] = birth_date
    if admission_year is not None:
        query["admission_year"] = admission_year
    if student_type:
        query["student_type"] = student_type
    if course is not None:
        query["course"] = course
    if program_name:
        query["program_name"] = program_name
    if faculty:
        query["faculty"] = faculty
    if group_name:
        query["group_name"] = group_name

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
        student_dict = student.model_dump(by_alias=True, exclude={"id"})

        # ──➤ приводим birthDate к datetime.datetime
        bd = student_dict.get("birthDate")
        if isinstance(bd, date):
            student_dict["birthDate"] = datetime.combine(bd, datetime.min.time())

        result = await db.students.insert_one(student_dict)
        created = await db.students.find_one({"_id": result.inserted_id})

        created["_id"] = str(created["_id"])
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
        raise HTTPException(status_code=400, detail="Invalid student ID")

    existing = await db.students.find_one({"_id": ObjectId(student_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student.model_dump(by_alias=True, exclude_unset=True)
    if update_data:
        await db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})

    updated = await db.students.find_one({"_id": ObjectId(student_id)})
    updated["_id"] = str(updated["_id"])

    return TypeAdapter(StudentWithStatistic).validate_python(updated)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID")

    result = await db.students.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
