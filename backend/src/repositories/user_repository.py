from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import ValidationError
from src.query_params import PaginationParams
from src.models.UserModel import UserModel
from src.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    DataCorruptionError,
)
from src.query_params.user_params import (
    UserFilterParams,
    UserSortParams,
)


async def save_user(
    user_model: UserModel,
    collection: AsyncIOMotorCollection,
) -> UserModel:
    # Check if user with the same  email already exists
    await ensure_email_unique(user_model.email, collection)

    # Insert the new user into the database
    result = await collection.insert_one(user_model.mongo_dump())
    user_model.id = result.inserted_id
    return user_model

async def ensure_email_unique(email, collection):
    existing = await collection.find_one({"email": email})
    if existing:
        raise UserAlreadyExistsError('User with this email already exists.')


async def get_user_by_id(
    user_id: str,
    collection: AsyncIOMotorCollection,
) -> UserModel:
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user ID")
    user = await collection.find_one({"_id": user_id})
    if not user:
        raise UserNotFoundError(f"User with id {user_id} not found.")
    return UserModel(**user)


async def update_user(
    user_id: str, updates: dict, collection: AsyncIOMotorCollection
) -> UserModel:
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid ObjectId")

    result = await collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": updates}
    )

    if result.matched_count == 0:
        raise UserNotFoundError()

    updated = await collection.find_one({"_id": ObjectId(user_id)})
    return UserModel(**updated)


async def delete_user(user_id: str, collection: AsyncIOMotorCollection) -> None:
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid ObjectId")

    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise UserNotFoundError()


async def get_list_users(
    filters: UserFilterParams,  # type: ignore
    sort: UserSortParams,
    pagination: PaginationParams,
    collection: AsyncIOMotorCollection,
) -> list[UserModel]:
    cursor = (
        collection.find(filters.to_mongo_filter())
        .sort(sort.to_mongo_sort())
        .skip(pagination.offset)
        .limit(pagination.limit)
    )
    try:
        users = []
        async for doc in cursor:
            users.append(UserModel(**doc))
    except ValidationError as e:
        raise DataCorruptionError(f"Invalid user data in DB: {e}")
    return users
