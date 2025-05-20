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
    user_id: PyObjectID,
    collection: AsyncIOMotorCollection,
) -> UserModel:
    user = await collection.find_one({"_id": user_id})
    if not user:
        raise UserNotFoundError(f"User with id {user_id} not found.")
    return UserModel(**user)
