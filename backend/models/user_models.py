from datetime import datetime, date
from sqlmodel import (
    Integer,
    Index,
    Column,
    DateTime,
    Field,
    SQLModel,
    Relationship,
    UniqueConstraint,
    String,
    Date,
    true,
    Boolean,
    false,
    JSON,
)
from typing import Optional, List

class User(SQLModel, table =True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str]= None
    display_name: Optional[str] = None
