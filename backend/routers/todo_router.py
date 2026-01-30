from models import Todo
from repositories.todo_repositories import TodoRepository
from fastapi import APIRouter, Depends, HTTPException
from schemas.todo_schemas import TodoSchema, TodoRegisterSchema
from db.db import get_session
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session
from helper.permission_helper import check_if_user_authenticated
from utils.jwt_utils import verify_token


todo_router = APIRouter(
    prefix = "/todo",
    tags = ["TODO APIs"]
)

@todo_router.put("/todos", response_model = TodoSchema)
def create_todo(
    payload : TodoSchema,
    session: Session = Depends(get_session),
    creds: dict = Depends(verify_token)
):
    user_details = check_if_user_authenticated(session, creds)
    if payload.id:
        existing_todo= TodoRepository.get_by_id(session, payload.id)
        if not existing_todo:
            raise HTTPException(status_code= HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "No TODO is there" )
        updated = TodoRepository.update(session, payload)
        session.commit()
        return updated
    else:
        todo = TodoRepository.create(session, Todo(
            todo = payload.todo,
            description = payload.description,
            user_id = user_details.id,
            is_completed = False
        ))
        session.commit()
        return todo
    

@todo_router.get("/todos", response_model = TodoRegisterSchema)
def get_all_todos(
    session: Session = Depends(get_session),
    creds: dict = Depends(verify_token)
):
    register_data = []
    user_details = check_if_user_authenticated(session, creds)
    todos = TodoRepository.get_all_by_columns(session, {'user_id': user_details.id})
    for todo in todos:
        register_data.append(todo)
    return TodoRegisterSchema(data=register_data)

