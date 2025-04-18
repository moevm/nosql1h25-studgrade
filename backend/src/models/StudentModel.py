from typing import Literal, Optional

from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from .PyObjectID import PyObjectId
from .StudentStatisticModel import StudentStatisticModel


class StudentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    birth_date: date
    admission_year: int
    student_type: Literal["bachelor", "master", "aspirant", "specialist"]
    course: int
    program_name: Literal[
        "Theoretical math", "Applied physics", "Computer science"
    ]
    faculty: Literal["Math", "Physics", "IT"]
    group_name: Literal["2323", "1421", "3501"]
    funding_type: Literal["budget", "contract"]
    statistic: StudentStatisticModel

    model_config = ConfigDict(
        populate_by_name=True,
    )
