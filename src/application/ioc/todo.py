from contextlib import asynccontextmanager
from uuid import UUID

from domain.models import EmptyTodo, TodoID, Todo

from application.interactors.create_todo import CreateTodo
from application.interactors.get_todo import GetTodo


class CTodoIoC:
    def __init__(self, todo_db_gateway):
        self._todo_db_gateway = todo_db_gateway

    @asynccontextmanager
    async def create_todo(self, todo: EmptyTodo, owner_uuid) -> TodoID:
        yield CreateTodo(
            empty_todo=todo,
            todo_db_gateway=self._todo_db_gateway,
            owner_id=owner_uuid
        )

    @asynccontextmanager
    async def get_todo(self, todo_id: UUID, owner_id: UUID) -> Todo:
        yield GetTodo(
            todo_id=todo_id,
            owner_id=owner_id,
            todo_db_gateway=self._todo_db_gateway
        )
