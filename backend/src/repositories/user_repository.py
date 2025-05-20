from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from src.models import PyObjectID
from src.models.UserModel import UserModel
from src.exceptions import UserAlreadyExistsError, UserNotFoundError


async def save_user(
    user_model: UserModel,
    collection: AsyncIOMotorCollection,
) -> UserModel:
    # Check if user with the same login or email already exists
    existing = await collection.find_one(
        {"$or": [{"login": user_model.login}, {"email": user_model.email}]}
    )
    if existing:
        raise UserAlreadyExistsError(
            'User with this login or email already exists.'
        )

    # Insert the new user into the database
    result = await collection.insert_one(user_model.mongo_dump())
    user_model.id = result.inserted_id
    return user_model

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
    user_id: str,
    updates: dict,
    collection: AsyncIOMotorCollection
) -> UserModel:
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid ObjectId")

    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updates}
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