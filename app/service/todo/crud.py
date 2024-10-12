from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models.models import TodoCreate, TodoUpdate, TodoInDB
from typing import List

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.todo_db 
collection = db.todos  

async def create_todo(todo: TodoCreate) -> TodoInDB:
    todo_dict = todo.dict()
    result = await collection.insert_one(todo_dict)
    return TodoInDB(id=str(result.inserted_id), **todo_dict)

async def read_todos() -> List[TodoInDB]:
    todos = []
    async for todo in collection.find():
        todos.append(TodoInDB(id=str(todo["_id"]), **todo))
    return todos

async def read_todo(todo_id: str) -> TodoInDB:
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        return None
    return TodoInDB(id=str(todo["_id"]), **todo)

async def update_todo(todo_id: str, todo: TodoUpdate) -> TodoInDB:
    update_data = todo.dict(exclude_unset=True)
    result = await collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    
    updated_todo = await collection.find_one({"_id": ObjectId(todo_id)})
    return TodoInDB(id=str(updated_todo["_id"]), **updated_todo)

async def delete_todo(todo_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    return result.deleted_count > 0

async def get_todos_by_category(category_name: str) -> List[TodoInDB]:
    todos = []
    async for todo in collection.find({"category": category_name}):
        todos.append(TodoInDB(id=str(todo["_id"]), **todo))
    return todos
