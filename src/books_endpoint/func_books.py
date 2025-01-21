from service.database import books_collection
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from app.oauth import get_current_user

async def get_books(current_user: dict = Depends(get_current_user)):
    books = await books_collection.find({}, {"_id": 0}).to_list(length=None)
    return books

async def get_book_by_name(book_name: str, current_user: dict = Depends(get_current_user)):
    book = await books_collection.find_one({"name": book_name}, {"_id": 0})
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book '{book_name}' not found"
        )
    return book

async def get_books_with_covers(current_user: dict = Depends(get_current_user)):
    books = await books_collection.find({}, {"_id": 0, "name": 1, "cover": 1}).to_list(length=None)
    return books


