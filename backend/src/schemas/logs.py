from typing import Optional
from datetime import date
from pydantic import BaseModel, ConfigDict, Field
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
    )


class LogCreate(BaseModel):
    user_id: PyObjectId
    action_type: str
    action_date: date
    ip_address: str
    affected_entity: str
    entity_id: PyObjectId
    description: str
    role: str

    model_config = ConfigDict(
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )


class LogUpdate(BaseModel):
    user_id: Optional[PyObjectId] = None
    action_type: Optional[str] = None
    action_date: Optional[date] = None
    ip_address: Optional[str] = None
    affected_entity: Optional[str] = None
    entity_id: Optional[PyObjectId] = None
    description: Optional[str] = None
    role: Optional[str] = None

class LogBulkCreateResponse(BaseModel):
    inserted_ids: list[str]