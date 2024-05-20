from uuid import UUID

from domain.exceptions import NotFoundError, NoteNotFoundError
from domain.models import Todo, Note


class GetNote:
    def __init__(
            self,
            owner_id: UUID,
            todo_id: UUID,
            note_id: UUID,
            note_db_gateway
    ):
        self._owner_id = owner_id
        self._todo_id = todo_id
        self._note_id = note_id
        self._note_db_gateway = note_db_gateway

    async def __call__(self) -> Note:
        try:
            result = await self._note_db_gateway.get_note(
                owner_id=self._owner_id,
                todo_id=self._todo_id,
                note_id=self._note_id
            )

            return result
        except NotFoundError as tnf:
            raise NoteNotFoundError from tnf
