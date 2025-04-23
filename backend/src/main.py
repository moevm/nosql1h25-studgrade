import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


# db
# db_url = "mongodb://user:password@mongo:27017/master?authSource=admin"
# client = AsyncIOMotorClient(db_url)
# db = client["master"]
# students_collection = db["students"]

# app
app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
