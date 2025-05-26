from typing import Optional

from .PyObjectID import PyObjectId
from pydantic import BaseModel, ConfigDict, Field
from .UserModel import UserModel

class TeacherModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    userId: PyObjectId
    assignedGroups: list[str]
    assignedSubjects: list[str]
    user: Optional[UserModel] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @classmethod
    def from_input(cls, teacher_in: "TeacherCreateSchema", userId: PyObjectId) -> "TeacherModel":
        return cls(
            userId=userId,
            assignedGroups=teacher_in.assignedGroups,
            assignedSubjects=teacher_in.assignedSubjects,
        )
        
    def mongo_dump(self) -> dict:
        data = self.model_dump(by_alias=True)
        if data.get("_id") is None:
            del data["_id"]
        return data
    
    def mongo_dump_with_user(self) -> dict:
        data = self.mongo_dump()
        if self.user is not None:
            user = self.user.mongo_dump()
        else:
            user = None
        return data, user

    
    def to_response_schema_with_user(self) -> "TeacherWithUserResponseSchema":
        if self.user is None:
            raise ValueError("User is not set in the TeacherModel instance.")
        return TeacherWithUserResponseSchema(
            id=str(self.id),
            userId=str(self.userId),
            assignedGroups=self.assignedGroups,
            assignedSubjects=self.assignedSubjects,
            user=self.user,
        )
    
from src.schemas.teachers import TeacherCreateSchema, TeacherWithUserResponseSchema