from contextlib import asynccontextmanager
from uuid import UUID

from domain.models import EmptyTodo, TodoID, Todo, DeletedResult

from application.interactors.create_todo import CreateTodo
from application.interactors.get_todo import GetTodo
from application.interactors.get_todo_notes import GetTodoNotes
from application.interactors.get_todos_owner import GetTodoOwner
from application.interactors.update_todo import UpdateTodo
from application.interactors.delete_todo import DeleteTodo

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

    @asynccontextmanager
    async def get_todo_notes(self, todo_id: UUID, owner_id: UUID) -> Todo:
        yield GetTodoNotes(
            todo_id=todo_id,
            owner_id=owner_id,
            todo_db_gateway=self._todo_db_gateway
        )

    @asynccontextmanager
    async def get_todos_owner(self, owner_id: UUID):
        yield GetTodoOwner(
            owner_id=owner_id,
            todo_db_gateway=self._todo_db_gateway
        )

    @asynccontextmanager
    async def update_todo(self, todo: EmptyTodo, owner_id: UUID, todo_id: UUID) -> Todo:
        yield UpdateTodo(
            owner_id=owner_id,
            todo_id=todo_id,
            empty_todo=todo,
            todo_db_gateway=self._todo_db_gateway
        )

    @asynccontextmanager
    async def delete_todo(self, todo_id: UUID, owner_id: UUID) -> DeletedResult:
        yield DeleteTodo(
            todo_id=todo_id,
            owner_id=owner_id,
            todo_db_gateway=self._todo_db_gateway
        )
