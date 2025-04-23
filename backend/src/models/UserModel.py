from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, StrictBool

from .PyObjectID import PyObjectId


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    email: str
    login: str
    password_hash: str
    first_name: str
    middle_name: str
    last_name: str
    active: StrictBool 
    role: str

    model_config = ConfigDict(
        populate_by_name=True,
    )
