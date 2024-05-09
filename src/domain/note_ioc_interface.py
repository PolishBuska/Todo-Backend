from abc import ABC, abstractmethod
from typing import List, Annotated
from uuid import UUID

from domain.models import EmptyNote, NoteID, Note, TodoID


class INoteIoC(ABC):

    @abstractmethod
    async def create_note(self, note: EmptyNote, owner_uuid, todo_id: Annotated[UUID, TodoID]) -> NoteID:
        raise NotImplementedError

    @abstractmethod
    async def get_note(self, note_id: NoteID, owner_uuid) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def update_note_status(self, status, note_id: NoteID, owner_uuid) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def list_notes(self, owner_id, todo_id: TodoID) -> List[Note]:
        raise NotImplementedError

    @abstractmethod
    async def edit_note(self, note: EmptyNote, owner_id, note_id: NoteID) -> Note:
        raise NotImplementedError
