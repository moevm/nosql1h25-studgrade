from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.TeacherModel import TeacherModel
from src.models.UserModel import UserModel
from src.schemas.teachers import TeacherCreateSchema
from src.exceptions import UserAlreadyExistsError

from src.repositories import user_repository
from src.db import db


async def create_teacher(
    teacher: TeacherCreateSchema,
    user_model: UserModel,
    teachers_collection: AsyncIOMotorCollection,
    users_collection: AsyncIOMotorCollection,
):
    await user_repository.ensure_email_unique(user_model.email, users_collection)

    async with await db.client.start_session() as session:
        async with session.start_transaction():
            user_result = await users_collection.insert_one(
                user_model.mongo_dump(), session=session
            )
            if user_result.inserted_id is None:
                raise UserAlreadyExistsError(
                    "User with this email already exists."
                )
            teacher_model = TeacherModel.from_input(
                teacher, user_result.inserted_id
            )
            result = await teachers_collection.insert_one(
                teacher_model.mongo_dump(), session=session
            )
    teacher_model.id = result.inserted_id
    user_model.id = user_result.inserted_id
    teacher_model.user = user_model
    teacher_model.userId = user_model.id

    return teacher_model


async def get_list_teachers(
    teacher_filters,
    user_filters,
    sort,
    pagination,
    teachers_collection: AsyncIOMotorCollection,
    users_collection: AsyncIOMotorCollection,
) -> list[TeacherModel]:
    teacher_filter = teacher_filters.to_mongo_filter()

    pipeline = [
        {"$match": teacher_filter},
        {
            "$lookup": {
                "from": users_collection.name,
                "let": {"user_id": "$userId"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": ["$_id", "$$user_id"]},
                            **user_filters.to_mongo_filter(),
                        }
                    }
                ],
                "as": "user",
            }
        },
        {"$unwind": "$user"},
        {"$sort": dict(sort.to_mongo_sort())},
        {"$skip": pagination.offset},
        {"$limit": pagination.limit},
    ]

    docs = await teachers_collection.aggregate(pipeline).to_list(length=None)

    return [TeacherModel(**doc) for doc in docs]
