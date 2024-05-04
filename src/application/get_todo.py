from domain.models import TodoID, Todo


class GetTodo:
    def __init__(
            self,
            owner_uuid,
            todo_id: TodoID,
            todo_db_gateway
    ):
        self._owner_uuid = owner_uuid
        self._todo_id = todo_id
        self._todo_db_gateway = todo_db_gateway

    async def __call__(self) -> Todo:
        result = await self._todo_db_gateway.get_todo(self._owner_uuid, self._todo_id)
        return result
