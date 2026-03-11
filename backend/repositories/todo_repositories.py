from .generic_respositories import CommonRepository
from models.todo_models import Todo

TodoRepository = CommonRepository(Todo)
