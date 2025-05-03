from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from .PyObjectID import PyObjectId

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # Делаем поле необязательным
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
        arbitrary_types_allowed=True  # Добавляем для работы с PyObjectId
    )

class UserBulkCreateResponse(BaseModel):
    inserted_ids: List[str]