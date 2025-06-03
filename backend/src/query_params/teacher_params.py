from typing import get_type_hints, Literal, Optional, TypeAlias
from pydantic import create_model, BaseModel, Field
from fastapi import Query
from pymongo import ASCENDING, DESCENDING
from src.schemas.teachers import TeacherBaseSchema

TeacherFilterFields = get_type_hints(TeacherBaseSchema)
TeacherSortableFields: TypeAlias = Literal[tuple(TeacherBaseSchema.model_fields.keys())]  # type: ignore
SortOrder: TypeAlias = Literal["asc", "desc"]


def to_mongo_filter(self) -> dict:
    return {k: v for k, v in self.model_dump(exclude_none=True).items()}


TeacherFilterParams = create_model(
    "TeacherFilterParams",
    **{
        name: (Optional[field_type], None)
        for name, field_type in TeacherFilterFields.items()
    }
)
TeacherFilterParams.to_mongo_filter = to_mongo_filter


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


