from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler: GetJsonSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.no_info_plain_validator_function(
                cls.validate
            ),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)
