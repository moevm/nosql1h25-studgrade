from typing import Optional

from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from .PyObjectID import PyObjectId


class LogModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    action_type: str
    action_date: date
    ip_address: str
    affected_entity: str
    entity_id: PyObjectId
    description: str
    role: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer('action_date')
    def serialize_action_date(self, action_date: date, _info):
        return datetime.combine(action_date, datetime.min.time())
