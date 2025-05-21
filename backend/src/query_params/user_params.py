from typing import Literal, Optional, TypeAlias, get_type_hints
from fastapi import Query
from pydantic import BaseModel, Field, create_model
from pymongo import ASCENDING, DESCENDING

from src.schemas.user import UserResponseSchema

UserFilterFields = get_type_hints(UserResponseSchema)
UserSortableFields: TypeAlias = Literal[tuple(UserResponseSchema.model_fields.keys())]  # type: ignore
SortOrder: TypeAlias = Literal["asc", "desc"]


def to_mongo_filter(self) -> dict:
    return {k: v for k, v in self.model_dump(exclude_none=True).items()}


UserFilterParams = create_model(
    "UserFilterSchema",
    **{
        name: (Optional[field_type], None)
        for name, field_type in UserFilterFields.items()
    }
)
UserFilterParams.to_mongo_filter = to_mongo_filter


class UserSortParams(BaseModel):
    sort_by: UserSortableFields = Field(default="lastName")
    sort_order: SortOrder = Field(default="asc")  # or "desc"

    def to_mongo_sort(self) -> list[tuple[str, int]]:
        direction = ASCENDING if self.sort_order == "asc" else DESCENDING
        return [(self.sort_by, direction)]


def get_user_sort_params(
    sort_by: UserSortableFields = Query("lastName"),
    sort_order: SortOrder = Query("asc"),
) -> UserSortParams:
    return UserSortParams(sort_by=sort_by, sort_order=sort_order)


class PaginationParams(BaseModel):
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


def get_pagination_params(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)
