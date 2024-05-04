from contextlib import asynccontextmanager

from domain.models import EmptyTodo, TodoID, Todo
from domain.todo_interactor_interface import ITodoInteractor

from application.create_todo import CreateTodo
from application.get_todo import GetTodo


class CTodoInteractor:
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
    async def get_todo(self, todo_id: TodoID, owner_uuid) -> Todo:
        yield GetTodo(
            todo_id=todo_id,
            owner_uuid=owner_uuid,
            todo_db_gateway=self._todo_db_gateway
        )
