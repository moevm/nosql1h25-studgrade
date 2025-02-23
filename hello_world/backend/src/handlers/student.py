import uuid

from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.student import (Student, StudentCreateRequest,
                              StudentCreateResponse)


def generate_uuid():
	return str(uuid.uuid4())


async def add_student(
		student_create_request: StudentCreateRequest,
		collection: AsyncIOMotorCollection
) -> StudentCreateResponse:
	student = Student(
		idx=generate_uuid(),
		first_name=student_create_request.first_name,
		last_name=student_create_request.last_name,
		birth_year=student_create_request.birth_year,
		group_number=student_create_request.group_number,
	)

	student_data = student.model_dump()
	await collection.insert_one(student_data)

	return StudentCreateResponse(idx=student.idx)


async def get_students(collection: AsyncIOMotorCollection) -> list[Student]:
	students = []
	cursor = collection.find()
	async for student in cursor:
		student["idx"] = str(student.pop("_id"))
		students.append(Student(**student))
	return students
