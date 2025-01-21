from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from src.books_endpoint.func_books import get_books, get_book_by_name, get_books_with_covers
from src.characters_endpoint.func_characters import get_characters, get_character_by_name, get_povbooks_by_character
from login.login import register_user, login_user, UserRegister
from app.oauth import get_current_user
import os

app = FastAPI()

host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
database = os.getenv("MONGO_DB")
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin")
db = client[database]
users_collection = db["users"]

@app.post("/register")
async def register(user: UserRegister):
    return await register_user(user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data)

@app.get("/books")
async def get_books_endpoint(current_user: dict = Depends(get_current_user)):
    books = await get_books()
    return books

@app.get("/books/covers")
async def get_books_with_covers_endpoint(current_user: dict = Depends(get_current_user)):
    books = await get_books_with_covers()
    return books

@app.get("/books/{book_name}")
async def get_book_by_name_endpoint(book_name: str, current_user: dict = Depends(get_current_user)):
    book = await get_book_by_name(book_name)
    return book

@app.get("/characters")
async def get_characters_endpoint(current_user: dict = Depends(get_current_user)):
    characters = await get_characters()
    return characters

@app.get("/characters/{character_name}")
async def get_character_by_name_endpoint(character_name: str, current_user: dict = Depends(get_current_user)):
    character = await get_character_by_name(character_name)
    return character

@app.get("/characters/{character_name}/povbooks")
async def get_povbooks_by_characters_endpoint(character_name: str, current_user: dict = Depends(get_current_user)):
    povbooks = await get_povbooks_by_character(character_name)
    return {"character": character_name, "povBooks": povbooks}


