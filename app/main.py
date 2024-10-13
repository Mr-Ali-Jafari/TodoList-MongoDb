from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from app.api.v1.todo.crud import router as todo_router
from app.api.v1.auth.auth_api import router as user_router
import os
from dotenv import load_dotenv

from pathlib import Path

dotenv_path = '.env'


app = FastAPI()

load_dotenv(dotenv_path=dotenv_path)


templates = Jinja2Templates(directory="app/templates")

app.include_router(todo_router, prefix="/api/v1/todo", tags=["todo"])
app.include_router(user_router, prefix="/api/v1/user", tags=["user"])

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.mongodb_client[DATABASE_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/todos")
async def todo_list(request: Request):
    db = request.app.mongodb
    todos = await db["todos"].find().to_list(100)
    return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos})
