import uvicorn
from fastapi import FastAPI
from .handlers.subjects.handler import router as subjects_router

app = FastAPI()

app.include_router(
    subjects_router,
    prefix="/subjects",
    tags=["subjects"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
