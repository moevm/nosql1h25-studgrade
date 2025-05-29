from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal, TYPE_CHECKING

from datetime import date
from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(str):

    @classmethod
    def __get_pydantic_core_schema__(cls, _s, _h):
        def validate(value):
            if isinstance(value, ObjectId):
                return str(value)
            if isinstance(value, str):
                try:
                    ObjectId(value)
                    return value
                except Exception as exc:  # noqa: BLE001
                    raise ValueError("Invalid ObjectId") from exc
            raise ValueError("Must be ObjectId or str")

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


class Student(BaseModel):
    """Core student document (without statistics)."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Анна",
                "lastName": "Смирнова",
                "birthDate": "2005-02-11",
                "admissionYear": 2023,
                "studentType": "bachelor",
                "course": 1,
                "programName": "Computer science",
                "faculty": "ФКТИ",
                "groupName": "2323",
                "userId": "5f8e9f9e9f9e9f9e9f9e9f9e",
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")

    user_id: Optional[PyObjectId] = Field(None, alias="userId")

    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    birth_date: date = Field(..., alias="birthDate")
    admission_year: int = Field(..., alias="admissionYear", ge=1900)

    student_type: Literal["bachelor", "master", "aspirant", "specialist"] = Field(
        ..., alias="studentType"
    )

    course: int = Field(..., ge=1, le=6)

    program_name: Literal[
        "Theoretical math",
        "Applied physics",
        "Computer science",
    ] = Field(..., alias="programName")

    faculty: Literal["ФКТИ", "ФИБС", "ГФ"]

    group_name: Literal["2323", "1421", "3501"] = Field(..., alias="groupName")


if TYPE_CHECKING:
    from src.schemas.subjects import SubjectStatModel
else:
    SubjectStatModel = "SubjectStatModel"  # type: ignore[assignment]


class StudentWithStatistic(Student):
    stats: Optional[List["SubjectStatModel"]] = Field(None, alias="stats")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                **Student.model_config["json_schema_extra"]["example"],
                "stats": [
                    {
                        "subjectId": "5f8d8f9d8f9d8f9d8f9d8f9d",
                        "totalLessons": 60,
                        "attendanceLessons": 52,
                        "year": 2024,
                        "season": "autumn",
                        "predictionScore": 4.7,
                        "score": 4.5,
                        "gradeValue": "5",
                    }
                ],
            }
        },
    )


class StudentBulkCreateResponse(BaseModel):
    inserted_ids: List[str]


if not TYPE_CHECKING:
    from src.schemas.subjects import SubjectStatModel

StudentWithStatistic.model_rebuild()
