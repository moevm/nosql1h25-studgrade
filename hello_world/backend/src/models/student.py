from pydantic import BaseModel


class StudentCreateRequest(BaseModel):
	first_name: str
	last_name: str
	birth_year: int
	group_number: str


class Student(BaseModel):
	idx: str  # uuid4
	first_name: str
	last_name: str
	birth_year: int
	group_number: str


class StudentCreateResponse(BaseModel):
	idx: str  # uuid4
