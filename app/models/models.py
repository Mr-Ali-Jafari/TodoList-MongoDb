from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TodoCreate(BaseModel):
    title: str
    is_done: bool = False
    category: str
    priority: Priority

class TodoUpdate(BaseModel):
    title: Optional[str]
    is_done: Optional[bool]
    category: Optional[str]
    priority: Optional[Priority]

class TodoInDB(TodoCreate):
    id: str  # MongoDB uses string IDs


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str