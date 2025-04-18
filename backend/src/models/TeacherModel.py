from typing import Optional

from .PyObjectID import PyObjectId
from pydantic import BaseModel, ConfigDict, Field


class TeacherModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    assigned_groups: list[str]
    assigned_subjects: list[PyObjectId]

    model_config = ConfigDict(
        populate_by_name=True,
    )
