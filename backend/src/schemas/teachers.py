from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Literal, Optional

from .PyObjectID import PyObjectId

from .user import UserCreateSchema, UserResponseSchema, UserBaseSchema


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


class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65f300c6b7c64b43c80b5aa1",
                "email": "teacher@example.com",
                "role": "teacher",
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    email: EmailStr
    role: str = "teacher"


class Teacher(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Ivan",
                "middleName": "Ivanovich",
                "lastName": "Ivanov",
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    first_name: str = Field(..., alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: str = Field(..., alias="lastName")

    user_id: Optional[PyObjectId] = Field(None, alias="userId")


class TeacherWithUser(Teacher):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65f31fa6b7c64b43c80b5aa2",
                "firstName": "Ivan",
                "middleName": "Ivanovich",
                "lastName": "Ivanov",
                "user": {
                    "_id": "65f300c6b7c64b43c80b5aa1",
                    "email": "teacher@example.com",
                    "role": "teacher",
                },
            }
        },
    )

    user: Optional[UserModel] = None


class TeacherBulkCreateResponse(BaseModel):
    inserted_ids: list[str]
