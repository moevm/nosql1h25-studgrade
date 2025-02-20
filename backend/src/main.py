import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from .handlers import add_student, get_students
from .models import Student, StudentCreateRequest, StudentCreateResponse

# db
db_url = "mongodb://user:password@mongo:27017/master?authSource=admin"
client = AsyncIOMotorClient(db_url)
db = client["master"]
students_collection = db["students"]

# app
app = FastAPI()


@app.post("/students/", response_model=StudentCreateResponse)
async def post_add_student(student_request: StudentCreateRequest):
	return await add_student(student_request, students_collection)


@app.get("/students/", response_model=list[Student])
async def get_all_students():
	return await get_students(students_collection)


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
