from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Literal, Optional

from .PyObjectID import PyObjectId

from .user import UserCreateSchema, UserResponseSchema, UserBaseSchema, UserUpdateSchema


class TeacherBaseSchema(UserBaseSchema):
    assignedGroups: list[str] = Field(
        default_factory=list,
        description="List of group IDs assigned to the teacher",
    )
    assignedSubjects: list[str] = Field(
        default_factory=list,
        description="List of subject IDs assigned to the teacher",
    )
    role: Literal["teacher"] = Field(
        default="teacher",
    )


class TeacherCreateSchema(TeacherBaseSchema, UserCreateSchema):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "firstName": "Ivan",
                "middleName": "Ivanovich",
                "lastName": "Ivanov",
                "email": "ivanovii@example.com",
                "password": "ivanovii123",
                "assignedGroups": ["group1", "group2"],
                "assignedSubjects": ["subject1", "subject2"],
            }
        },
    )


class TeacherWithUserResponseSchema(TeacherBaseSchema, UserResponseSchema):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "_id": "65f31fa6b7c64b43c80b5aa2",
                "firstName": "Ivan",
                "middleName": "Ivanovich",
                "lastName": "Ivanov",
                "email": "ivanovii@example.com",
                "role": "teacher",
                "assignedGroups": ["group1", "group2"],
                "assignedSubjects": ["subject1", "subject2"],
            },
        },
    )

class TeacherUpdateSchema(UserUpdateSchema):
    assignedGroups: Optional[list[str]] = Field(
        default=None,
        description="List of group IDs assigned to the teacher",
    )
    assignedSubjects: Optional[list[str]] = Field(
        default=None,
        description="List of subject IDs assigned to the teacher",
    )
    role: Optional[Literal["teacher"]] = Field(
        default=None,
    )
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "firstName": "Olga",
                "middleName": "Ivanovna",
                "lastName": "Sidorova",
                "email": "o.sidorova@example.com",
                "role": "teacher",
                "assignedGroups": ['2381', '2343'],
                "assignedSubjects": ["subject1", "subject2"],
            }
        },
    )

