from uuid import UUID

from src.domain.models import Note, NoteIdList
from src.domain.exceptions import NotFoundError, NoteNotFoundByPk

from src.application.common.uow import Commiter


class ConfirmNotes:
    def __init__(self, note_id_dto: NoteIdList, note_db_gateway, commiter: Commiter, todo_id: UUID):
        self._note_confirmation = note_id_dto
        self._note_db_gateway = note_db_gateway
        self._commiter = commiter
        self._todo_id = todo_id

    async def __call__(self) -> Note:
        try:
            res = await self._note_db_gateway.confirm_notes(
                note_confirmation=self._note_confirmation,
                todo_id=self._todo_id
            )
            await self._commiter.commit()
            return res
        except NotFoundError as nfe:
            await self._commiter.rollback()
            raise NoteNotFoundByPk from nfe
