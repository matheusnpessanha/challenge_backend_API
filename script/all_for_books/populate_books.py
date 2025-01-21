import json
import motor.motor_asyncio
import asyncio
import os

async def get_db():

    host = os.getenv("MONGO_HOST")
    port = int(os.getenv("MONGO_PORT"))
    database = os.getenv("MONGO_DB")
    username = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASS")

    client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource={'admin'}")
    db = client[database]  
    return db


async def insert_books_data():
    db = await get_db()  
    collection = db["books"]  

    
    with open("script/all_for_books/books_with_characters.json", "r") as json_file:
        books_data = json.load(json_file)

    
    for book in books_data:
        result = await collection.insert_one(book)
        print(f"Livro inserido com ID: {result.inserted_id}")


async def main():
    await insert_books_data()

if __name__ == "__main__":
    asyncio.run(main())
