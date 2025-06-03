from motor.motor_asyncio import AsyncIOMotorClient

db_url = "mongodb://user:password@db:27017/master?authSource=admin&replicaSet=rs0"
client = AsyncIOMotorClient(db_url)
db = client["master"]
