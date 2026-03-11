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
from typing import Optional, List, Dict, Any


class HistoryOfChanges(SQLModel, table = True):
    __tablename__ = "history_of_changes"

    id :Optional[int] = Field(default=None, primary_key=True)
    record :int
    changes_json: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )
    operation : str
    user_id : int
    display_name : str


