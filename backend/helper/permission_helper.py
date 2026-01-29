from fastapi import HTTPException
from sqlmodel import Session
from repositories.user_repositories import UserRepo

def check_if_user_authenticated(session: Session, creds: dict):
    username = creds.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    existing_user = UserRepo.get_by_column(session, filters={"username": username})
    if not existing_user:
        raise HTTPException(status_code=401, detail="User not found")
    return existing_user