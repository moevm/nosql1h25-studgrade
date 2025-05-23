from typing import Optional, List, Literal
from fastapi import APIRouter, HTTPException, Query, status
from bson import ObjectId
from pydantic import TypeAdapter

from src.schemas.teachers import Teacher, TeacherWithUser, TeacherBulkCreateResponse
from src.db import db
from src.utils.security import generate_random_password, hash_password

router = APIRouter()



@router.get("/", response_model=List[TeacherWithUser])
async def get_all_teachers(
    first_name: Optional[str] = Query(None, alias="first_name"),
    middle_name: Optional[str] = Query(None, alias="middle_name"),
    last_name: Optional[str] = Query(None, alias="last_name"),
    limit: Optional[int] = Query(10, gt=0),
    offset: Optional[int] = Query(0, ge=0),
    sort_by: Optional[str] = Query("lastName"),
    order: Optional[Literal["asc", "desc"]] = Query("asc"),
):

    query: dict = {}
    if first_name:
        query["firstName"] = {"$regex": first_name, "$options": "i"}
    if middle_name:
        query["middleName"] = {"$regex": middle_name, "$options": "i"}
    if last_name:
        query["lastName"] = {"$regex": last_name, "$options": "i"}

    sort_order = 1 if order == "asc" else -1
    allowed_sort_fields = ["firstName", "middleName", "lastName", "createdAt"]
    sort_field = sort_by if sort_by in allowed_sort_fields else "lastName"

    cursor = (
        db.teachers
        .find(query)
        .sort(sort_field, sort_order)
        .skip(offset)
        .limit(limit)
    )

    teachers = await cursor.to_list(length=None)
    for t in teachers:
        t["_id"] = str(t["_id"])
        if "userId" in t and isinstance(t["userId"], ObjectId):
            t["userId"] = str(t["userId"])

    adapter = TypeAdapter(List[TeacherWithUser])
    return adapter.validate_python(teachers)


@router.post("/", response_model=TeacherWithUser, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: Teacher):
    try:
        user_id, raw_pwd = await _create_linked_user(teacher)

        teacher_dict = teacher.model_dump(by_alias=True, exclude={"id", "user_id"})
        teacher_dict["userId"] = ObjectId(user_id)

        async with await db.client.start_session() as s:
            async with s.start_transaction():
                res = await db.teachers.insert_one(teacher_dict, session=s)

        created = await db.teachers.find_one({"_id": res.inserted_id})
        created["_id"] = str(created["_id"])
        created["rawPassword"] = raw_pwd
        created["user"] = await db.users.find_one({"_id": ObjectId(user_id)}, {"passwordHash": 0})
        created["user"]["_id"] = str(created["user"]["_id"])
        return created

    except Exception as e:
        raise HTTPException(500, f"Database operation failed: {e}")


@router.get("/{teacher_id}", response_model=TeacherWithUser)
async def get_teacher(teacher_id: str):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(400, "Invalid teacher ID")

    teacher = await db.teachers.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(404, "Teacher not found")

    teacher["_id"] = str(teacher["_id"])
    if "userId" in teacher and isinstance(teacher["userId"], ObjectId):
        teacher["userId"] = str(teacher["userId"])

    return TypeAdapter(TeacherWithUser).validate_python(teacher)


@router.patch("/{teacher_id}", response_model=TeacherWithUser)
async def update_teacher(teacher_id: str, teacher: Teacher):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(400, "Invalid teacher ID")

    existing = await db.teachers.find_one({"_id": ObjectId(teacher_id)})
    if not existing:
        raise HTTPException(404, "Teacher not found")

    upd = teacher.model_dump(by_alias=True, exclude_unset=True)
    if not upd:
        return TypeAdapter(TeacherWithUser).validate_python(existing | {"_id": teacher_id})

    async with await db.client.start_session() as s:
        async with s.start_transaction():
            await db.teachers.update_one({"_id": ObjectId(teacher_id)}, {"$set": upd}, session=s)

            user_updates = {}
            for field, alias in [
                ("first_name", "firstName"),
                ("middle_name", "middleName"),
                ("last_name", "lastName"),
            ]:
                if field in teacher.__fields_set__:
                    user_updates[alias] = getattr(teacher, field)
            if user_updates:
                await db.users.update_one({"_id": existing["userId"]}, {"$set": user_updates}, session=s)

    updated = await db.teachers.find_one({"_id": ObjectId(teacher_id)})
    updated["_id"] = str(updated["_id"])
    updated["user"] = await db.users.find_one({"_id": existing["userId"]}, {"passwordHash": 0})
    updated["user"]["_id"] = str(updated["user"]["_id"])
    return TypeAdapter(TeacherWithUser).validate_python(updated)


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id: str):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(400, "Invalid teacher ID")

    teacher = await db.teachers.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(404, "Teacher not found")
        async with await db.client.start_session() as s:
            async with s.start_transaction():
                await db.teachers.delete_one({"_id": ObjectId(teacher_id)}, session=s)
                await db.users.delete_one({"_id": teacher["userId"]}, session=s)

@router.post(
    "/bulk/",
    response_model=TeacherBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["teachers", "bulk"],
)
async def bulk_create_teachers(teachers: List[Teacher]):
    try:
        teachers_dicts = []

        async with await db.client.start_session() as s:
            async with s.start_transaction():
                for t in teachers:
                    user_id, _ = await _create_linked_user(t)

                    d = t.model_dump(by_alias=True, exclude={"id", "user_id"})
                    d["userId"] = ObjectId(user_id)
                    teachers_dicts.append(d)

                result = await db.teachers.insert_many(teachers_dicts, session=s)

        return TeacherBulkCreateResponse(inserted_ids=[str(i) for i in result.inserted_ids])

    except Exception as e:
        raise HTTPException(500, f"Bulk create failed: {e}")


def _generate_login(first_name: str, last_name: str) -> str:
    return f"{first_name[0].lower()}.{last_name.lower()}"


async def _create_linked_user(teacher: Teacher) -> tuple[str, str]:
    raw_pwd = generate_random_password()
    pwd_hash = hash_password(raw_pwd)

    login = _generate_login(teacher.first_name, teacher.last_name)
    email = f"{login}@example.com"

    user_dict = {
        "firstName": teacher.first_name,
        "middleName": teacher.middle_name,
        "lastName": teacher.last_name,
        "login": login,
        "email": email,
        "passwordHash": pwd_hash,
        "role": "teacher",
    }
    res = await db.users.insert_one(user_dict)
    return str(res.inserted_id), raw_pwd
