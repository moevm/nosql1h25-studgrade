from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
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


class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65f300c6b7c64b43c80b5aa1",
                "email": "teacher@example.com",
                "role": "teacher"
            }
        },
    )

    id: Optional[PyObjectId] = Field(None, alias="_id")
    email: EmailStr
    role: str = "teacher"


class Teacher(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True,
        json_schema_extra={"example": {
            "firstName": "Ivan", "middleName": "Ivanovich",
            "lastName": "Ivanov"
        }},
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
                    "role": "teacher"
                }
            }
        },
    )

    user: Optional[UserModel] = None


class TeacherBulkCreateResponse(BaseModel):
    inserted_ids: list[str]
