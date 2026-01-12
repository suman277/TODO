from models import Todo
from repositories.todo_repositories import TodoRepository
from fastapi import APIRouter, Depends, HTTPException
from schemas.todo_schemas import TodoSchema
from db.db import get_session
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session


todo_router = APIRouter(
    prefix = "/todo",
    tags = ["TODO APIs"]
)

@todo_router.put("/todos", response_model = TodoSchema)
def create_todo(
    payload : TodoSchema,
    session: Session = Depends(get_session),
):

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
            user_id = payload.user_id,
            is_completed = False
        ))
        session.commit()
        return todo


