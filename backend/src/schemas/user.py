from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, Literal, List

from .PyObjectID import PyObjectId

Role = Literal["student", "teacher", "admin"]


class UserCreateSchema(BaseModel):
    firstName: str
    middleName: Optional[str]
    lastName: str
    login: str
    email: EmailStr
    password: str
    role: Role = Field(
        "student", description="User role; defaults to student"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Olga",
                "middleName": "Ivanovna",
                "lastName": "Sidorova",
                "login": "o.sidorova",
                "email": "o.sidorova@example.com",
                "role": "student",
            }
        },
    )
    
class UserResponseSchema(BaseModel):
    id: str
    firstName: str
    middleName: Optional[str]
    lastName: str
    login: str
    email: EmailStr
    role: Role
    


class User(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firstName": "Olga",
                "middleName": "Ivanovna",
                "lastName": "Sidorova",
                "login": "o.sidorova",
                "email": "o.sidorova@example.com",
                "role": "teacher",
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")

    first_name: str = Field(..., alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: str = Field(..., alias="lastName")

    login: str
    email: EmailStr
    role: Literal["student", "teacher", "admin"] = Field(
        "student", description="User role; defaults to student"
    )


class UserBulkCreateResponse(BaseModel):
    inserted_ids: List[str]


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",  # Запрещает неизвестные поля
    )

    first_name: Optional[str] = Field(None, alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: Optional[str] = Field(None, alias="lastName")
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["student", "teacher", "admin"]] = None
