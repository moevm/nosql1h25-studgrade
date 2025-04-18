from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from .SubjectStatModel import SubjectStatModel


class StudentStatisticModel(BaseModel):
    average_score: Decimal
    attendance_percent: Decimal
    calculation_date: date
    count_activities: int
    exlusion_probability: Decimal
    subjects: list[SubjectStatModel]

