from abc import ABC, abstractmethod
from typing import List, Annotated
from uuid import UUID

from domain.models import EmptyTodo, TodoID, Todo


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
    async def list_todos(self, owner_uuid, owner_id) -> List[Todo]:
        raise NotImplementedError

    @abstractmethod
    async def edit_todo(self, todo: EmptyTodo, owner_id, todo_id: TodoID) -> Todo:
        raise NotImplementedError
