from fastapi import HTTPException, status
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.security import OAuth2PasswordRequestForm
from app.oauth import create_access_token
from pydantic import BaseModel, EmailStr
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr = None  

host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
database = os.getenv("MONGO_DB")
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin")

db = client[database]
users_collection = db["users"]

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def register_user(user: UserRegister):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = hash_password(user.password)
    new_user = {
        "username": user.username,
        "password": hashed_password,
        "email": user.email,
    }
    
    result = await users_collection.insert_one(new_user)
    if result.inserted_id:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user",
        )

async def login_user(form_data: OAuth2PasswordRequestForm):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"access_token": access_token}}
    )
    return {"access_token": access_token, "token_type": "bearer"}
