from models.user_models import User
from schemas.user_schemas import UserSchema, TokenResponse, UserLoginSchema
from repositories.user_repositories import UserRepo
from fastapi import APIRouter, Depends, HTTPException
from db.db import get_session
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlmodel import Session
import bcrypt
from utils.common_utils import genearte_password_hash
from datetime import datetime
from utils.jwt_utils import jwt_utils, verify_token
from helper.permission_helper import check_if_user_authenticated

user_router = APIRouter(
    prefix = "/user",
    tags = ["User APIs"])

@user_router.put("/users", response_model = UserSchema)
def create_user(
    payload : UserSchema,
    session: Session = Depends(get_session),
    creds: dict = Depends(verify_token)
):
    check_if_user_authenticated(session, creds)
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
            password = genearte_password_hash(payload.password),
            email = payload.email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ))
        session.commit()
        return user

@user_router.post("/login", response_model = TokenResponse)
def login_user(
    payload : UserLoginSchema,
    session: Session = Depends(get_session),
):
    existing_user = UserRepo.get_by_column(session, filters={"username": payload.username})
    if not existing_user:
        raise HTTPException(status_code= HTTP_500_INTERNAL_SERVER_ERROR, 
        detail = "Invalid Username" )
    
    if not bcrypt.checkpw(
        payload.password.encode("utf-8"),
        existing_user.password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    token = jwt_utils.create_access_token(username=existing_user.username)
    print(session.__dict__)
    return {
        "access_token": token,
        "token_type": "bearer"
    }