from typing import Optional, Literal

from .PyObjectID import PyObjectId
from pydantic import BaseModel, ConfigDict, Field
from .UserModel import UserModel
from src.utils.security import hash_password


class TeacherModel(UserModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    role: Literal['teacher'] = 'teacher'
    assignedGroups: list[str]
    assignedSubjects: list[str]

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @classmethod
    def from_input(
        cls,
        teacher_in: "TeacherCreateSchema",
    ) -> "TeacherModel":
        return cls(
            firstName=teacher_in.firstName,
            middleName=teacher_in.middleName,
            lastName=teacher_in.lastName,
            email=teacher_in.email,
            role='teacher',
            password_hash=hash_password(teacher_in.password),
            assignedGroups=teacher_in.assignedGroups,
            assignedSubjects=teacher_in.assignedSubjects,
        )

    def mongo_dump(self) -> dict:
        data = self.model_dump(by_alias=True)
        if data.get("_id") is None:
            del data["_id"]
        return data

    def to_response_schema(self) -> "TeacherWithUserResponseSchema":
        return TeacherWithUserResponseSchema(
            id=str(self.id),
            firstName=self.firstName,
            middleName=self.middleName,
            lastName=self.lastName,
            email=self.email,
            role=self.role,
            assignedGroups=self.assignedGroups,
            assignedSubjects=self.assignedSubjects,
        )

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
