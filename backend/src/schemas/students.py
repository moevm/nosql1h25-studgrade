from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal
from datetime import date
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
                except Exception:
                    raise ValueError("Invalid ObjectId")
            raise ValueError("Must be ObjectId or str")

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


try:
    from src.schemas.subjects import SubjectStatModel  # type: ignore
except ImportError:
    class SubjectStatModel(BaseModel):
        subject_id: PyObjectId
        total_lessons: int
        attendance_lessons: int
        year: int
        season: Literal["autumn", "spring"]
        prediction_score: float
        score: float
        grade_value: Optional[Literal["pass", "fail", "5", "4", "3"]]

        model_config = ConfigDict(populate_by_name=True)


class Student(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Иван",
                "lastName": "Иванов",
                "birthDate": "2005-09-14",
                "admissionYear": 2023,
                "studentType": "bachelor",
                "course": 2,
                "programName": "Computer science",
                "faculty": "IT",
                "groupName": "2323"
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")

    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    birth_date: date = Field(..., alias="birthDate")
    admission_year: int = Field(..., alias="admissionYear", ge=1900, le=date.today().year)

    student_type: Literal["bachelor", "master", "aspirant", "specialist"] = Field(
        ..., alias="studentType"
    )

    course: int = Field(..., ge=1, le=6)

    program_name: Literal[
        "Theoretical math",
        "Applied physics",
        "Computer science",
    ] = Field(..., alias="programName")

    faculty: Literal["Math", "Physics", "IT"]
    group_name: Literal["2323", "1421", "3501"] = Field(..., alias="groupName")


class StudentWithStatistic(Student):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Иван",
                "lastName": "Иванов",
                "birthDate": "2005-09-14",
                "admissionYear": 2023,
                "studentType": "bachelor",
                "course": 2,
                "programName": "Computer science",
                "faculty": "IT",
                "groupName": "2323",
                "stats": [
                    {
                        "subjectId": "5f8d8f9d8f9d8f9d8f9d8f9d",
                        "totalLessons": 60,
                        "attendanceLessons": 52,
                        "year": 2024,
                        "season": "autumn",
                        "predictionScore": 4.7,
                        "score": 4.5,
                        "gradeValue": "5"
                    }
                ]
            }
        },
    )

    stats: Optional[List[SubjectStatModel]] = Field(None, alias="stats")

class StudentBulkCreateResponse(BaseModel):
    inserted_ids: List[str]