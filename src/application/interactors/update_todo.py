from uuid import UUID

from domain.exceptions import TodoNotFoundError, TodoNotFoundByPk
from src.domain.models import EmptyTodo, Todo


class UpdateTodo:
    def __init__(self, empty_todo: EmptyTodo, todo_db_gateway, owner_id: UUID, todo_id: UUID):
        self._todo = empty_todo
        self._todo_db_gateway = todo_db_gateway
        self._owner_id = owner_id
        self._todo_id = todo_id

    async def __call__(self) -> Todo:
        try:
            todo = await self._todo_db_gateway.update_todo(
                todo=self._todo,
                owner_id=self._owner_id,
                todo_id=self._todo_id
            )
            return todo
        except TodoNotFoundError as tnf:
            raise TodoNotFoundByPk from tnf
