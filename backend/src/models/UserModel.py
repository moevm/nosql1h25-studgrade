from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from passlib.context import CryptContext

from src.utils.security import hash_password
from .PyObjectID import PyObjectId




class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    firstName: str
    middleName: Optional[str] = Field(default=None)
    lastName: str
    email: EmailStr
    role: str
    password_hash: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    def from_input(cls, user_in: "UserCreateSchema") -> "UserModel":
        return cls(
            firstName=user_in.firstName,
            middleName=user_in.middleName,
            lastName=user_in.lastName,
            email=user_in.email,
            role=user_in.role,
            password_hash=hash_password(user_in.password),
        )

    def mongo_dump(self) -> dict:
        data = self.model_dump(by_alias=True)
        if data.get("_id") is None:
            del data["_id"]
        return data

    def to_response_schema(self) -> "UserResponseSchema":
        return UserResponseSchema(
            id=str(self.id),
            firstName=self.firstName,
            middleName=self.middleName,
            lastName=self.lastName,
            email=self.email,
            role=self.role,
        )


from src.schemas.user import UserCreateSchema, UserResponseSchema
