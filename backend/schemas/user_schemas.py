from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserSchema(SQLModel, table = False):
    id: Optional[int] = Field(default=None)
    username: Optional[str]= None
    display_name: Optional[str] = None
    password : str
    email: Optional[str] = None


class TokenResponse(SQLModel, table = False):
    access_token: str
    token_type: str = "bearer"

class UserLoginSchema(SQLModel, table = False):
    username: str
    password : str