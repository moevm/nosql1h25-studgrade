from motor.motor_asyncio import AsyncIOMotorClient

db_url = "mongodb://user:password@mongo:27017/master?authSource=admin"
client = AsyncIOMotorClient(db_url)
db = client["master"]
