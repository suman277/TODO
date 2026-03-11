from datetime import datetime
from sqlmodel import (
    Field,
    SQLModel,
    Column,
    DateTime,
)
import sqlalchemy.sql.functions as func
from typing import Optional, List

class User(SQLModel, table =True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str]= None
    display_name: Optional[str] = None
    password : str
    email: Optional[str] = None
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            index=True,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            index=True,
        )
    )
