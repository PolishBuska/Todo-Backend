from contextlib import asynccontextmanager
from uuid import UUID

from domain.models import EmptyNote, NoteID, TodoID, Note
from src.application.interactors.create_note import CreateNote
from src.application.interactors.get_note import GetNote


class CNoteIoC:
    def __init__(self, note_db_gateway):
        self._note_db_gateway = note_db_gateway

    @asynccontextmanager
    async def create_note(self, note: EmptyNote, owner_id, todo_id: TodoID) -> NoteID:
        yield CreateNote(
            note_db_gateway=self._note_db_gateway,
            empty_note=note,
            owner_id=owner_id,
            todo_id=todo_id
        )

    @asynccontextmanager
    async def get_note(self, note_id: UUID, todo_id: UUID, owner_id: UUID) -> Note:
        yield GetNote(
            note_db_gateway=self._note_db_gateway,
            note_id=note_id,
            todo_id=todo_id,
            owner_id=owner_id
        )
