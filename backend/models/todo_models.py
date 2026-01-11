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

class Todo(SQLModel, table =True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    todo: str
    description: Optional[str] = None
    user_id: int = Field(foreign_key= 'users.id')
    is_completed: bool = Field(default=False)