from contextlib import asynccontextmanager
from uuid import UUID

from src.domain.models import EmptyTodo, TodoID, Todo, DeletedResult, TodoNotesStatusDTO

from src.application.interactors.create_todo import CreateTodo
from src.application.interactors.get_todo import GetTodo
from src.application.interactors.get_todo_notes import GetTodoNotes
from src.application.interactors.get_todos_owner import GetTodoOwner
from src.application.interactors.update_todo import UpdateTodo
from src.application.interactors.delete_todo import DeleteTodo
from src.application.interactors.confirm_todo import ConfirmTodo


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
    async def get_todo_notes(self, todo_notes_query_dto: TodoNotesStatusDTO, owner_id: UUID) -> Todo:
        yield GetTodoNotes(
            todo_notes_status_dto=todo_notes_query_dto,
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

    @asynccontextmanager
    async def confirm_todo(self, todo_id: UUID, owner_id: UUID) -> Todo:
        yield ConfirmTodo(
            todo_id=todo_id,
            owner_id=owner_id,
            todo_db_gateway=self._todo_db_gateway
        )

