from uuid import UUID

from domain.exceptions import TodoNotFoundError, TodoNotFoundByPk
from src.domain.models import DeletedResult


class DeleteTodo:
    def __init__(self, todo_db_gateway, owner_id: UUID, todo_id: UUID):
        self._todo_db_gateway = todo_db_gateway
        self._owner_id = owner_id
        self._todo_id = todo_id

    async def __call__(self) -> DeletedResult:
        try:
            todo = await self._todo_db_gateway.delete_todo(
                owner_id=self._owner_id,
                todo_id=self._todo_id
            )
            return todo
        except TodoNotFoundError as tnf:
            raise TodoNotFoundByPk from tnf
