from app.models.models import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException

async def create_user(db, user: UserCreate):
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    await db["users"].insert_one(user_data)
    return user_data

async def authenticate_user(db, user_login: UserLogin):
    user = await db["users"].find_one({"username": user_login.username})
    if not user or not verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user
