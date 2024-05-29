from abc import ABC, abstractmethod
from typing import List, Annotated
from uuid import UUID

from domain.models import EmptyNote, NoteID, Note, TodoID, IdentityOwnership, NoteIdList


class INoteIoC(ABC):

    @abstractmethod
    async def create_note(self, note: EmptyNote, owner_id, todo_id: UUID) -> NoteID:
        raise NotImplementedError

    @abstractmethod
    async def get_note(self, todo_id: UUID, note_id: UUID, owner_id: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def update_note_status(self, status, note_id: NoteID, owner_uuid: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def list_notes(self, owner_id: UUID, todo_id: TodoID) -> List[Note]:
        raise NotImplementedError

    @abstractmethod
    async def update_note(self, note: EmptyNote, owner_id: UUID, note_id: UUID, todo_id: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def delete_note(self, owner_id: UUID, note_id: UUID, todo_id: UUID) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def confirm_note(self, identity_ownership: IdentityOwnership, todo_id: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def confirm_notes(self, identity_ownership_list: NoteIdList, todo_id: UUID) -> List[Note]:
        raise NotImplementedError
