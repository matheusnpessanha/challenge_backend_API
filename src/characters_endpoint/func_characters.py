from service.database import characters_collection
from fastapi import HTTPException, Depends
from app.oauth import get_current_user

async def get_characters(current_user: dict = Depends(get_current_user)):
    characters = await characters_collection.find({}, {"_id": 0}).to_list(length=None)
    return characters

async def get_character_by_name(character_name: str, current_user: dict = Depends(get_current_user)):
    character = await characters_collection.find_one(
        {"name": {"$regex": f"^{character_name}$", "$options": "i"}},
        {"_id": 0}
    )
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return character

async def get_povbooks_by_character(character_name: str, current_user: dict = Depends(get_current_user)):
    print(f"Received character_name: {character_name}")
    character = await characters_collection.find_one(
        {"name": {"$regex": f"^{character_name}$", "$options": "i"}},
        {"_id": 0, "povBooks": 1}
    )
    if not character:
        raise HTTPException(status_code=404, detail=f"Character '{character_name}' not found")
    
    povbooks = character.get("povBooks", [])
    if not povbooks:
        raise HTTPException(status_code=404, detail=f"Character '{character_name}' has no POV books")
    
    return povbooks


