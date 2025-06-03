from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import ValidationError

from src.exceptions import DataCorruptionError
from src.models.TeacherModel import TeacherModel
from src.models.UserModel import UserModel
from src.exceptions import UserAlreadyExistsError
from src.query_params import PaginationParams
from src.query_params.teacher_params import (
    TeacherFilterParams,
    TeacherSortParams,
)

from src.repositories import user_repository
from src.db import db


async def create_teacher(
    teacher_model: TeacherModel,
    teachers_collection: AsyncIOMotorCollection,
):
    await user_repository.ensure_email_unique(
        teacher_model.email, teachers_collection
    )

    result = await teachers_collection.insert_one(teacher_model.mongo_dump())
    teacher_model.id = result.inserted_id
    return teacher_model


async def get_list_teachers(
    teacher_filters: TeacherFilterParams, 
    sort: TeacherSortParams,
    pagination: PaginationParams,
    teachers_collection: AsyncIOMotorCollection,
) -> list[TeacherModel]:
    cursor = (
        teachers_collection
        .find(teacher_filters.to_mongo_filter() | {"role": "teacher"})
        .sort(sort.to_mongo_sort())
        .skip(pagination.offset)
        .limit(pagination.limit)
    )
    
    try:
        teachers = []
        async for doc in cursor:
            teachers.append(TeacherModel(**doc))
    except ValidationError as e:
        raise DataCorruptionError(f"Data corruption error") from e
            


    return teachers
