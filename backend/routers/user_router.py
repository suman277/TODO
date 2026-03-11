from models.user_models import User
from schemas.user_schemas import UserSchema, TokenResponse, UserLoginSchema, LogRequestSchema, LogSchema, Info
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
from repositories.hoc_repository import HistoryOfChangesRepo
from utils.common_utils import fix_audit_log

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
        existing_user = UserRepo.get_by_column(session, payload.username)
        if existing_user:
            raise HTTPException(
                status_code = HTTP_500_INTERNAL_SERVER_ERROR,
                deatils = "Username already exists"
            )
        user = UserRepo.create(session, User(
            username = payload.username,
            display_name = payload.username,
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
        "token_type": "Bearer"
    }

@user_router.get("/log/{id}", response_model = LogRequestSchema)
def create_user(
    id:int,
    session: Session = Depends(get_session),
    creds: dict = Depends(verify_token)
):
    query_obj = {}
    user_details=check_if_user_authenticated(session, creds)
    query_obj["user_id"]: user_details.id
    if not (id == user_details.id):
            raise HTTPException(status_code = HTTP_500_INTERNAL_SERVER_ERROR, detail = "No logs are there")
    existing_logs= HistoryOfChangesRepo.get_all_by_columns(session, query_obj)
    if not existing_logs:
        raise HTTPException(status_code= HTTP_500_INTERNAL_SERVER_ERROR, 
        detail = "No logs are there" )
    # audit_logs = existing_logs.model_dump 
    logs=fix_audit_log(existing_logs)
    return LogRequestSchema(logs = logs)


@user_router.get("/info", response_model = Info)
def get_user(
    session: Session = Depends(get_session),
    creds: dict = Depends(verify_token)
):
    user_details=check_if_user_authenticated(session, creds)
    return Info(
        user_id = user_details.id,
        name = user_details.username
    )

        