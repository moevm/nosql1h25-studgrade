import uvicorn
from fastapi import FastAPI
from .handlers.subjects.handler import router as subjects_router
from .handlers.students.handler import router as students_router
from .handlers.teachers.handler import router as teachers_router
from .handlers.logs.handler import router as log_router


app = FastAPI()

app.include_router(
    subjects_router,
    prefix="/subjects",
    tags=["subjects"]
)

app.include_router(
    students_router,
    prefix="/students",
    tags=["students"]
)

app.include_router(
    teachers_router,
    prefix="/teachers",
    tags=["teachers"]
)

app.include_router(
    log_router,
    prefix="/logs",
    tags=["logs"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
