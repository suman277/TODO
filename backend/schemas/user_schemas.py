from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class UserSchema(SQLModel, table = False):
    id: Optional[int] = Field(default=None)
    username: Optional[str]= None
    display_name: Optional[str] = None
    password : str
    email: Optional[str] = None


class TokenResponse(SQLModel, table = False):
    access_token: str
    token_type: str = "Bearer"

class UserLoginSchema(SQLModel, table = False):
    username: str
    password : str

class LogSchema(SQLModel, table = False):
    record : int
    changes_json : Optional[dict] = None
    operation: str
    user_id : int
    display_name : str

class LogRequestSchema(SQLModel, table = False):
    logs : List[LogSchema]