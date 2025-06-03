from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from pydantic import ValidationError

from src.query_params import PaginationParams, get_pagination_params
from src.query_params.user_params import (
    UserFilterParams,
    UserSortParams,
    get_user_sort_params,
)
from src.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.repositories import user_repository
from src.models import UserModel
from src.db.dependencies import get_users_collection
from src.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

router = APIRouter()


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
        user = await user_repository.get_user_by_id(ObjectId(user_id), collection)
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
    user_id: str,
    update_data: UserUpdateSchema,
    collection=Depends(get_users_collection),
):
    update_dict = update_data.model_dump(exclude_none=True)

    try:
        updated_user: UserModel = await user_repository.update_user(
            user_id, update_dict, collection
        )
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
    user_id: str, collection=Depends(get_users_collection)
):
    try:
        await user_repository.delete_user(user_id, collection)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=list[UserResponseSchema])
async def list_users_endpoint(
    filters: UserFilterParams = Depends(),  # type: ignore
    pagination: PaginationParams = Depends(get_pagination_params),
    sort: UserSortParams = Depends(get_user_sort_params),
    collection=Depends(get_users_collection),
):

    user_models = await user_repository.get_list_users(
        filters, sort, pagination, collection
    )
    try:
        return [user.to_response_schema() for user in user_models]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal error while serializing users" + str(e),
        )
