from contextlib import asynccontextmanager

from domain.models import EmptyNote, NoteID, TodoID
from src.application.interactors.create_note import CreateNote


class CNoteIoC:
    def __init__(self, note_db_gateway):
        self._note_db_gateway = note_db_gateway

    @asynccontextmanager
    async def create_note(self, note: EmptyNote, owner_uuid, todo_id: TodoID) -> NoteID:
        yield CreateNote(
            note_db_gateway=self._note_db_gateway,
            empty_note=note,
            owner_id=owner_uuid,
            todo_id=todo_id
        )

