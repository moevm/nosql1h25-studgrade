from typing import Optional, List, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId
from pydantic import TypeAdapter, ValidationError

from src.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.repositories import user_repository
from src.models import UserModel
from src.db import db
from src.db.dependencies import get_users_collection
from src.schemas.user import (
    User,
    UserBulkCreateResponse,
    UserCreateSchema,
    UserResponseSchema,
    UserUpdate,
    UserUpdateSchema,
)

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_all_users(
    first_name: Optional[str] = Query(None),
    middle_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    login: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    role: Optional[Literal["student", "teacher", "admin"]] = Query(None),
    limit: Optional[int] = Query(10, gt=0),
    offset: Optional[int] = Query(0, ge=0),
    sort_by: Optional[str] = Query("lastName"),
    order: Optional[Literal["asc", "desc"]] = Query("asc"),
):
    query = {}

    if first_name:
        query["firstName"] = {"$regex": first_name, "$options": "i"}
    if middle_name:
        query["middleName"] = {"$regex": middle_name, "$options": "i"}
    if last_name:
        query["lastName"] = {"$regex": last_name, "$options": "i"}

    if login:
        query["login"] = {"$regex": login, "$options": "i"}
    if email:
        query["email"] = {"$regex": email, "$options": "i"}

    if role:
        query["role"] = role

    # Sorting
    allowed_sort_fields = [
        "firstName",
        "middleName",
        "lastName",
        "login",
        "email",
        "role",
    ]
    sort_field = sort_by if sort_by in allowed_sort_fields else "lastName"
    sort_order = 1 if order == "asc" else -1

    cursor = (
        db.users.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
    )
    users = await cursor.to_list(length=None)
    for user in users:
        user["_id"] = str(user["_id"])

    adapter = TypeAdapter(List[User])
    return adapter.validate_python(users)


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreateSchema, collection=Depends(get_users_collection)
):  
    try:
        user_model = UserModel.from_input(user)
        saved_user = await user_repository.save_user(user_model, collection)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed: {str(e)}",
        )

    return saved_user.to_response_schema()


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: str, collection=Depends(get_users_collection)):
    try:
        user = await user_repository.get_user_by_id(
            ObjectId(user_id), collection)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return user.to_response_schema()
    
@router.patch("/{user_id}", response_model=UserResponseSchema)
async def update_user_endpoint(
    user_id: str ,
    update_data: UserUpdateSchema,
    collection = Depends(get_users_collection),
):
    update_dict = update_data.model_dump(exclude_none=True)

    try:
        updated_user: UserModel = await user_repository.update_user(user_id, update_dict, collection)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {str(e)}",
        )

    return updated_user.to_response_schema()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: str,
    collection = Depends(get_users_collection)
):
    try:
        await user_repository.delete_user(user_id, collection)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


