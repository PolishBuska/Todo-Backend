from uuid import UUID

from domain.models import IdentityOwnership, Note
from domain.exceptions import NotFoundError, NoteNotFoundByPk

from application.common.uow import Commiter


class ConfirmNote:
    def __init__(self, identity_ownership: IdentityOwnership, note_db_gateway, commiter: Commiter, todo_id: UUID):
        self._note_confirmation = identity_ownership
        self._note_db_gateway = note_db_gateway
        self._commiter = commiter
        self._todo_id = todo_id

    async def __call__(self) -> Note:
        try:
            res = await self._note_db_gateway.confirm_note(
                note_confirmation=self._note_confirmation,
                todo_id=self._todo_id
            )
            await self._commiter.commit()
            return res
        except NotFoundError as nfe:
            await self._commiter.rollback()
            raise NoteNotFoundByPk from nfe
