from fastapi import APIRouter, Depends, Request
from app.service.auth.auth_service import create_user, authenticate_user
from app.models.models import UserCreate, UserLogin, Token
from app.utils.security import create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, request: Request):
    db = request.app.mongodb
    await create_user(db, user)
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, request: Request):
    db = request.app.mongodb
    user_in_db = await authenticate_user(db, user)
    access_token = create_access_token({"sub": user_in_db["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
