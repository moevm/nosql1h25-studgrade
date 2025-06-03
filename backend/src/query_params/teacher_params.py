from typing import get_type_hints, Literal, Optional, TypeAlias
from pydantic import create_model, BaseModel, Field, EmailStr
from fastapi import Query
from pymongo import ASCENDING, DESCENDING
from src.schemas.teachers import TeacherBaseSchema

TeacherFilterFields = get_type_hints(TeacherBaseSchema)
TeacherSortableFields: TypeAlias = Literal[tuple(TeacherBaseSchema.model_fields.keys())]  # type: ignore
SortOrder: TypeAlias = Literal["asc", "desc"]


class TeacherFilterParams(BaseModel):
    firstName: Optional[str]
    middleName: Optional[str] = Field(
        default=None,
        description="Middle name of the user",
    )
    lastName: Optional[str]
    email: Optional[EmailStr]
    role: Optional[Literal['teacher']]
    assignedGroups: list[str] = Field(
        default_factory=list,
        description="List of group IDs assigned to the teacher",
    )
    assignedSubjects: list[str] = Field(
        default_factory=list,
        description="List of subject IDs assigned to the teacher",
    )

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

def get_teacher_filter_params(
    firstName: Optional[str] = Query(None),
    middleName: Optional[str] = Query(
        default=None,
        description="Middle name of the user",
    ),
    lastName: Optional[str] = Query(None),
    email: Optional[EmailStr] = Query(None),
    role: Optional[Literal['teacher']] = Query(None),
    assignedGroups: list[str] = Query(
        default_factory=list,
        description="List of group IDs assigned to the teacher",
    ),
    assignedSubjects: list[str] = Query(
        default_factory=list,
        description="List of subject IDs assigned to the teacher",
    ),

):
    return TeacherFilterParams(
        firstName=firstName,
        middleName=middleName,
        lastName=lastName,
        email=email,
        role=role,
        assignedGroups=assignedGroups,
        assignedSubjects=assignedSubjects
    )

class TeacherSortParams(BaseModel):
    sort_by: TeacherSortableFields = Field(default="userId")
    sort_order: SortOrder = Field(default="asc")

    def to_mongo_sort(self) -> list[tuple[str, int]]:
        direction = ASCENDING if self.sort_order == "asc" else DESCENDING
        return [(self.sort_by, direction)]


def get_teacher_sort_params(
    sort_by: TeacherSortableFields = Query("lastName"),
    sort_order: SortOrder = Query("asc"),
) -> TeacherSortParams:
    return TeacherSortParams(sort_by=sort_by, sort_order=sort_order)


