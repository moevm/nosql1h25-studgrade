from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from .PyObjectID import PyObjectId


class SubjectMetaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    subject_name: str
    description: str
    grade_type: Literal["pass/fail", "exam"]
    is_activity: StrictBool 

    model_config = ConfigDict(
        populate_by_name=True,
    )
