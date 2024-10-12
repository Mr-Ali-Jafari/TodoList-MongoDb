from fastapi import FastAPI
from app.api.v1.todo.crud import router as todo_router

app = FastAPI()

app.include_router(todo_router, prefix="/todos", tags=["todos"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API"}
