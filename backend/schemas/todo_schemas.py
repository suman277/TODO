from sqlmodel import SQLModel
from typing import Optional, Dict

class TodoSchema(SQLModel, table = False):
    id: Optional[int] = None
    todo : str
    description: str
    user_id : Optional[int] = None
    is_completed : bool

class TodoRegisterSchema(SQLModel, table = False):
    data : list[TodoSchema] = None
