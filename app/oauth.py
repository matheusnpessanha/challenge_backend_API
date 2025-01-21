from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
database = os.getenv("MONGO_DB")
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#client = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin")
#client = AsyncIOMotorClient(f"mongodb://{username}:{password}@localhost:27017/{database}?authSource=admin")
client = AsyncIOMotorClient(f"mongodb://{username}:{password}@api_got:27017/{database}?authSource=admin")

db = client[database]
users_collection = db["users"]


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.info(f"Validating token: {token}")
    user = await users_collection.find_one({"access_token": token})
    if not user:
        logger.warning(f"Invalid token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"User authenticated: {user['username']}")
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user.get("email"),
        "roles": user.get("roles", []),
    }
