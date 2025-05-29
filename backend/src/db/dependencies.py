from motor.motor_asyncio import AsyncIOMotorCollection

from .db import db


def get_users_collection() -> AsyncIOMotorCollection:
    return db["users"]

def get_teachers_collection() -> AsyncIOMotorCollection:
    return db["teachers"]