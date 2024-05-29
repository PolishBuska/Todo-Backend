from typing import List
from uuid import UUID
from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from domain.models import EmptyNote, TodoID, Note, IdentityOwnership, NoteIdList
from domain.exceptions import NoteIntegrityError, NotFoundError


class NoteGateway:
    def __init__(self, session: AsyncSession, model):
        self._session = session
        self._model = model

    async def create_note(self, note: EmptyNote, owner_id, todo_id: TodoID):
        try:
            stmt = insert(self._model).values(
                name=note.name,
                content=note.content,
                owner_id=owner_id,
                todo_id_fk=todo_id
            ).returning(self._model)
            result = await self._session.execute(stmt)
            await self._session.commit()
            result = result.scalar()
            return Note(**result.to_dict())
        except IntegrityError as ie:
            raise NoteIntegrityError from ie

    async def get_note(self, note_id: UUID, todo_id: UUID, owner_id: UUID) -> Note:
        query = select(self._model).where(
            (self._model.note_id == note_id) & (self._model.todo_id_fk == todo_id) &
            (self._model.owner_id == owner_id)
        )
        res = await self._session.scalar(query)
        if not res:
            raise NotFoundError
        return Note(**res.to_dict())

    async def update_note(self, note: EmptyNote, note_id: UUID, todo_id: UUID, owner_id: UUID) -> Note:
        stmt = update(self._model).values(name=note.name, content=note.content).where(
            (self._model.todo_id_fk == todo_id) & (self._model.note_id == note_id)
            & (self._model.owner_id == owner_id)
        ).returning(self._model)
        res = await self._session.execute(stmt)
        if not res:
            raise NotFoundError
        res = res.scalar()
        await self._session.commit()
        return Note(**res.to_dict())

    async def delete_note(self, note_id: UUID, todo_id: UUID, owner_id: UUID) -> UUID:
        stmt = delete(self._model).where(
            (self._model.note_id == note_id) &
            (self._model.todo_id_fk == todo_id) &
            (self._model.owner_id == owner_id)
        ).returning(self._model.note_id)
        res = await self._session.execute(stmt)
        await self._session.commit()
        res = res.scalar()
        if not res:
            raise NotFoundError
        return res

    async def confirm_note(self, note_confirmation: IdentityOwnership, todo_id: UUID) -> Note:
        stmt = update(self._model).where(
            (self._model.note_id == note_confirmation.note_id) &
            (self._model.owner_id == note_confirmation.owner_id) &
            (self._model.todo_id_fk == todo_id)
        ).values(status=True).returning(self._model)
        res = await self._session.execute(stmt)
        if not res:
            raise NotFoundError
        await self._session.flush()
        res = res.scalar()
        return Note(**res.to_dict())

    async def confirm_notes(self, note_confirmation: NoteIdList, todo_id: UUID) -> List[Note]:
        stmt = update(self._model).where(

            (self._model.note_id.in_([note["note_id"] for note in note_confirmation.notes])) &
            (self._model.owner_id.in_([note["owner_id"] for note in note_confirmation.notes])) &
            (self._model.todo_id_fk == todo_id)
        ).values(status=True).returning(self._model)

        res = await self._session.execute(stmt)

        res = res.scalars().all()
        if not res:
            raise NotFoundError
        return [note.to_dict() for note in res]
