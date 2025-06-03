from typing import Literal, Optional, TypeAlias, get_type_hints
from fastapi import Query
from pydantic import BaseModel, Field, create_model, EmailStr
from pymongo import ASCENDING, DESCENDING

from src.schemas.user import UserBaseSchema, Role

UserFilterFields = get_type_hints(UserBaseSchema)
UserSortableFields: TypeAlias = Literal[tuple(UserBaseSchema.model_fields.keys())]  # type: ignore
SortOrder: TypeAlias = Literal["asc", "desc"]


class UserFilterParams(BaseModel):
    firstName: Optional[str]
    middleName: Optional[str] = Field(
        default=None,
        description="Middle name of the user",
    )
    lastName: Optional[str]
    email: Optional[EmailStr]
    role: list[Role] = Field(default_factory=list, description="User role; defaults to student")

    def to_mongo_filter(self) -> dict:
        filters = {}
        for k, v in self.model_dump(exclude_none=True).items():
            if isinstance(v, str):
                v = {"$regex": v}
            elif isinstance(v, list):
                if not v:
                    continue
                v =  {"$in" : v} 
            filters[k] = v
        return filters

def get_user_filter_params(
    firstName: Optional[str] = Query(None),
    middleName: Optional[str] = Query(
        default=None,
        description="Middle name of the user",
    ),
    lastName: Optional[str] = Query(None),
    email: Optional[EmailStr] = Query(None),
    role: list[Role] = Query(default_factory=list),

):
    return UserFilterParams(
        firstName=firstName,
        middleName=middleName,
        lastName=lastName,
        email=email,
        role=role,
    )

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




