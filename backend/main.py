from fastapi import FastAPI
from dotenv import load_dotenv
from sqlmodel import SQLModel

from routers.todo_router import todo_router
from routers.user_router import user_router

load_dotenv()

app = FastAPI(title="Todo API")

app.include_router(todo_router)
app.include_router(user_router)