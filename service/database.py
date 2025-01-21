from motor.motor_asyncio import AsyncIOMotorClient
import os


host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
database = os.getenv("MONGO_DB")
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

class Database:
    client: AsyncIOMotorClient = None

db = Database()

MONGO_URL = f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource={'admin'}"

client = AsyncIOMotorClient(MONGO_URL)
database = client.get_database(database) 
books_collection = database["books"]  
characters_collection = database["characters"]  