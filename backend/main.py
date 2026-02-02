from fastapi import FastAPI
from dotenv import load_dotenv
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from routers.todo_router import todo_router
from routers.user_router import user_router

load_dotenv()

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)
app.include_router(user_router)