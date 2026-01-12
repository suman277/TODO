from models.user_models import User
from schemas.user_schemas import UserSchema
from repositories.user_repositories import UserRepo
from fastapi import APIRouter, Depends, HTTPException
from db.db import get_session
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session
from datetime import datetime

user_router = APIRouter(
    prefix = "/user",
    tags = ["User APIs"])

@user_router.put("/users", response_model = UserSchema)
def create_user(
    payload : UserSchema,
    session: Session = Depends(get_session),
):

    if payload.id:
        existing_user= UserRepo.get_by_id(session, payload.id)
        if not existing_user:
            raise HTTPException(status_code= HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "No User is there" )
        updated = UserRepo.update(session, payload)
        session.commit()
        return updated
    else:
        user = UserRepo.create(session, User(
            username = payload.username,
            display_name = payload.display_name,
            password = payload.password,
            email = payload.email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ))
        session.commit()
        return user