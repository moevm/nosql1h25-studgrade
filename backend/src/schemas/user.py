from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, Literal

from .PyObjectID import PyObjectId

Role = Literal["student", "teacher", "admin"]


class UserBaseSchema(BaseModel):
    firstName: str
    middleName: Optional[str] = Field(
        default=None,
        description="Middle name of the user",
    )
    lastName: str
    email: EmailStr
    role: Role = Field("student", description="User role; defaults to student")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
    )


class UserCreateSchema(UserBaseSchema):
    password: str

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
                "password": "sidorova123",
            }
        },
    )


class UserResponseSchema(UserBaseSchema):
    id: PyObjectId

    model_config = ConfigDict(
        extra="forbid",
    )


class UserUpdateSchema(BaseModel):
    firstName: Optional[str]
    middleName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    role: Optional[Role]

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
