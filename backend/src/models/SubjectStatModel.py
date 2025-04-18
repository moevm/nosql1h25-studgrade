from typing import Literal, Optional

from decimal import Decimal
from pydantic import BaseModel
from .PyObjectID import PyObjectId


class SubjectStatModel(BaseModel):
    subject_id: PyObjectId
    total_lessons: int
    attendance_lessons: int
    year: int
    season: Literal["autumn", "spring"]
    prediction_score: Decimal
    score: Decimal
    grade_value: Optional[Literal["pass", "fail", "5", "4", "3", None]]
