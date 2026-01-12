from sqlmodel import SQLModel
from typing import Optional, Dict

class TodoSchema(SQLModel, table = False):
    id: Optional[int] = None
    todo : str
    description: str
    user_id : int
    is_completed : bool
