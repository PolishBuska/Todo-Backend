from uuid import UUID

from src.domain.exceptions import TodoNotFoundError, TodoNotFoundByPk
from src.domain.models import Todo


class GetTodoOwner:
    def __init__(
            self,
            owner_id: UUID,
            todo_db_gateway
    ):
        self._owner_id = owner_id
        self._todo_db_gateway = todo_db_gateway

    async def __call__(self) -> Todo:
        try:
            result = await self._todo_db_gateway.get_todos_owner(owner_id=self._owner_id)

            return result
        except TodoNotFoundError as tnf:
            raise TodoNotFoundByPk from tnf
