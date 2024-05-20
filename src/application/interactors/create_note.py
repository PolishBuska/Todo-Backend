from src.domain.models import EmptyNote, Note, TodoID

from domain.exceptions import NoteIntegrityError, NoteAlreadyExist


class CreateNote:
    def __init__(self, empty_note: EmptyNote, note_db_gateway, owner_id, todo_id: TodoID):
        self._note = empty_note
        self._note_db_gateway = note_db_gateway
        self._owner_id = owner_id
        self._todo_id = todo_id

    async def __call__(self) -> Note:
        try:
            todo = await self._note_db_gateway.create_note(
                note=self._note,
                owner_id=self._owner_id,
                todo_id=self._todo_id
            )
            return todo
        except NoteIntegrityError as nie:
            raise NoteAlreadyExist from nie
