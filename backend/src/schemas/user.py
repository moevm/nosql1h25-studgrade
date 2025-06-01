from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, Literal

from .PyObjectID import PyObjectId

Role = Literal["student", "teacher", "admin"]


class UserCreateSchema(BaseModel):
    firstName: str
    middleName: Optional[str]
    lastName: str
    email: EmailStr
    password: str
    role: Role = Field("student", description="User role; defaults to student")

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
                "role": "student",
            }
        },
    )


class UserResponseSchema(BaseModel):
    id: PyObjectId
    firstName: str
    middleName: Optional[str]
    lastName: str
    email: EmailStr
    role: Role

    model_config = ConfigDict(
        extra="forbid",
    )


class UserUpdateSchema(BaseModel):
    firstName: Optional[str] = Field(default=None)
    middleName: Optional[str] = Field(default=None)
    lastName: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    role: Optional[Role] = Field(default=None)

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
            }
        },
    )
