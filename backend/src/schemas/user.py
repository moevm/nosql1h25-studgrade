from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, Literal, List
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
                "role": "teacher"
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
        extra="forbid"  # Запрещает неизвестные поля
    )

    first_name: Optional[str] = Field(None, alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: Optional[str] = Field(None, alias="lastName")
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["student", "teacher", "admin"]] = None
