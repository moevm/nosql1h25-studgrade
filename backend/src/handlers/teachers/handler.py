from typing import Optional, List, Literal
from fastapi import APIRouter, HTTPException, Query, status
from bson import ObjectId
from pydantic import TypeAdapter

from src.schemas.teachers import Teacher, TeacherWithUser
from src.db import db


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
        teacher_dict = teacher.model_dump(by_alias=True, exclude={"id"})
        result = await db.teachers.insert_one(teacher_dict)
        created = await db.teachers.find_one({"_id": result.inserted_id})

        if created:
            created["_id"] = str(created["_id"])
            if "userId" in created and isinstance(created["userId"], ObjectId):
                created["userId"] = str(created["userId"])

        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {e}")


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

    update_data = teacher.model_dump(by_alias=True, exclude_unset=True)
    if not update_data:
        return TypeAdapter(TeacherWithUser).validate_python({"_id": teacher_id, **existing})

    await db.teachers.update_one({"_id": ObjectId(teacher_id)}, {"$set": update_data})

    updated = await db.teachers.find_one({"_id": ObjectId(teacher_id)})
    updated["_id"] = str(updated["_id"])
    if "userId" in updated and isinstance(updated["userId"], ObjectId):
        updated["userId"] = str(updated["userId"])

    return TypeAdapter(TeacherWithUser).validate_python(updated)


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id: str):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(400, "Invalid teacher ID")

    result = await db.teachers.delete_one({"_id": ObjectId(teacher_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Teacher not found")
