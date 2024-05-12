from abc import ABC, abstractmethod
from typing import List, Annotated
from uuid import UUID

from domain.models import EmptyTodo, TodoID, Todo, DeletedResult


class ITodoIoC(ABC):

    @abstractmethod
    async def create_todo(self, todo: EmptyTodo, owner_uuid) -> TodoID:
        raise NotImplementedError

    @abstractmethod
    async def get_todo(self, todo_id: UUID, owner_id: UUID) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def update_todo_status(self, status, todo_id: TodoID, owner_uuid) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def get_todo_notes(self, todo_id: UUID, owner_id: UUID) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def get_todos_owner(self, owner_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def update_todo(self, todo: EmptyTodo, todo_id: UUID, owner_id: UUID) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def delete_todo(self, todo_id: UUID, owner_id: UUID) -> DeletedResult:
        raise NotImplementedError
