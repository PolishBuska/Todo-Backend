from contextlib import asynccontextmanager
from typing import List
from uuid import UUID

from domain.models import EmptyNote, NoteID, TodoID, Note, IdentityOwnership, NoteIdList
from application.interactors.create_note import CreateNote
from application.interactors.get_note import GetNote
from application.interactors.update_note import UpdateNote
from application.interactors.delete_note import DeleteNote
from application.interactors.confirm_note import ConfirmNote
from application.interactors.confirm_notes import ConfirmNotes


class CNoteIoC:
    def __init__(self, note_db_gateway, commiter):
        self._note_db_gateway = note_db_gateway
        self._commiter = commiter

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

    @asynccontextmanager
    async def update_note(self, note_id: UUID, owner_id: UUID, note: EmptyNote, todo_id: UUID) -> Note:
        yield UpdateNote(
            note_db_gateway=self._note_db_gateway,
            note_id=note_id,
            todo_id=todo_id,
            owner_id=owner_id,
            note=note
        )

    @asynccontextmanager
    async def delete_note(self, note_id: UUID, owner_id: UUID, todo_id: UUID) -> UUID:
        yield DeleteNote(
            note_db_gateway=self._note_db_gateway,
            note_id=note_id,
            todo_id=todo_id,
            owner_id=owner_id
        )

    @asynccontextmanager
    async def confirm_note(self, identity_ownership: IdentityOwnership, todo_id: UUID) -> Note:
        yield ConfirmNote(
            identity_ownership=identity_ownership,
            note_db_gateway=self._note_db_gateway,
            commiter=self._commiter,
            todo_id=todo_id
        )

    @asynccontextmanager
    async def confirm_notes(self, identity_ownership_list: NoteIdList, todo_id: UUID) -> List[Note]:
        yield ConfirmNotes(
            note_id_dto=identity_ownership_list,
            commiter=self._commiter,
            note_db_gateway=self._note_db_gateway,
            todo_id=todo_id

        )
