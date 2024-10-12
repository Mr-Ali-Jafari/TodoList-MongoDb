from fastapi import APIRouter, HTTPException
from app.service.todo.crud import (
    create_todo,
    read_todos,
    read_todo,
    update_todo,
    delete_todo,
    get_todos_by_category,
)
from app.models.models import TodoCreate, TodoUpdate, TodoInDB
from typing import List
router = APIRouter()

@router.post("/", response_model=TodoInDB)
async def create_todo_endpoint(todo: TodoCreate):
    return await create_todo(todo)

@router.get("/", response_model=List[TodoInDB])
async def read_todos_endpoint():
    return await read_todos()

@router.get("/{todo_id}", response_model=TodoInDB)
async def read_todo_endpoint(todo_id: str):
    todo = await read_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo_endpoint(todo_id: str, todo: TodoUpdate):
    updated_todo = await update_todo(todo_id, todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found or nothing to update")
    return updated_todo

@router.delete("/{todo_id}")
async def delete_todo_endpoint(todo_id: str):
    success = await delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted"}

@router.get("/category/{category_name}", response_model=List[TodoInDB])
async def get_todos_by_category_endpoint(category_name: str):
    return await get_todos_by_category(category_name)
