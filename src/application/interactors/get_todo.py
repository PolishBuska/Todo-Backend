from uuid import UUID

from domain.models import TodoID, Todo


class GetTodo:
    def __init__(
            self,
            owner_id: UUID,
            todo_id: UUID,
            todo_db_gateway
    ):
        self._owner_id = owner_id
        self._todo_id = todo_id
        self._todo_db_gateway = todo_db_gateway

    async def __call__(self) -> Todo:
        result = await self._todo_db_gateway.get_todo(owner_id=self._owner_id, todo_id=self._todo_id)

        return result
