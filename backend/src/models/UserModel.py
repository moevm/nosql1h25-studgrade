from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from passlib.context import CryptContext
from .PyObjectID import PyObjectId


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    firstName: str
    middleName: str
    lastName: str
    login: str
    email: EmailStr
    role: str
    password_hash: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    @classmethod
    def from_input(cls, user_in: "UserCreateSchema") -> "UserModel":
        return cls(
            firstName=user_in.firstName,
            middleName=user_in.middleName,
            lastName=user_in.lastName,
            login=user_in.login,
            email=user_in.email,
            role=user_in.role,
            password_hash=password_context.hash(user_in.password)
        )
        
    def mongo_dump(self) -> dict:
        data = self.model_dump(by_alias=True)
        if data.get("_id") is None:
            del data["_id"]
        return data
        

from src.schemas.user import UserCreateSchema