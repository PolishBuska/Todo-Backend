from uuid import UUID

from domain.exceptions import NoteNotFoundError, NoteNotFoundByPk
from src.domain.models import Note, EmptyNote


class UpdateNote:
    def __init__(self, note: EmptyNote, note_db_gateway, owner_id: UUID, todo_id: UUID, note_id: UUID):
        self._note = note
        self._note_db_gateway = note_db_gateway
        self._owner_id = owner_id
        self._todo_id = todo_id
        self._note_id = note_id

    async def __call__(self) -> Note:
        try:
            todo = await self._note_db_gateway.update_note(
                note=self._note,
                owner_id=self._owner_id,
                todo_id=self._todo_id,
                note_id=self._note_id
            )
            return todo
        except NoteNotFoundError as tnf:
            raise NoteNotFoundByPk from tnf
