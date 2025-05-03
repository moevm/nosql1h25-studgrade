from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal
from decimal import Decimal
from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        def validate(value):
            if isinstance(value, ObjectId):
                return str(value)
            if isinstance(value, str):
                try:
                    ObjectId(value)
                    return value
                except:
                    raise ValueError("Invalid ObjectId")
            raise ValueError("Must be ObjectId or str")

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


class SubjectStatModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "subjectId": "5f8d8f9d8f9d8f9d8f9d8f9d",
                "totalLessons": 30,
                "attendanceLessons": 25,
                "year": 2023,
                "season": "autumn",
                "predictionScore": 4.5,
                "score": 4.2,
                "gradeValue": "5"
            }
        }
    )

    subject_id: PyObjectId = Field(..., alias="subjectId")
    total_lessons: int = Field(..., alias="totalLessons")
    attendance_lessons: int = Field(..., alias="attendanceLessons")
    year: int
    season: Literal["autumn", "spring"]
    prediction_score: float = Field(..., alias="predictionScore")
    score: float
    grade_value: Optional[Literal["pass", "fail", "5", "4", "3"]] = Field(None, alias="gradeValue")


class SubjectMeta(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Mathematics",
                "description": "Advanced mathematics course",
                "stats": []
            }
        }
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    description: Optional[str] = None
    stats: Optional[List[SubjectStatModel]] = None


class SubjectBulkCreateResponse(BaseModel):
    inserted_ids: List[str]