from src.domain.exceptions import TodoIntegrityError, TodoAlreadyExist
from src.domain.models import EmptyTodo, Todo


class CreateTodo:
    def __init__(self, empty_todo: EmptyTodo, todo_db_gateway, owner_id):
        self._todo = empty_todo
        self._todo_db_gateway = todo_db_gateway
        self._owner_id = owner_id

    async def __call__(self) -> Todo:
        try:
            todo = await self._todo_db_gateway.create_todo(self._todo, self._owner_id)
            return todo
        except TodoIntegrityError as tie:
            raise TodoAlreadyExist from tie
