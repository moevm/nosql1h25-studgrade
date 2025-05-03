from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.user import UserModel, UserBulkCreateResponse
from src.db import db
from bson import ObjectId
from pydantic import TypeAdapter

router = APIRouter()


@router.post(
    "/bulk/",
    response_model=UserBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk create users",
    tags=["users", "bulk"]
)
async def bulk_create_users(users: List[UserModel]):
    try:
        users_dicts = [user.model_dump(by_alias=True, exclude_none=True) for user in users]
        result = await db.users.insert_many(users_dicts)
        return UserBulkCreateResponse(inserted_ids=[str(id) for id in result.inserted_ids])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk create operation failed: {str(e)}"
        )