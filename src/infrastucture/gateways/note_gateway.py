from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from domain.models import EmptyNote, TodoID


class NoteGateway:
    def __init__(self, session: AsyncSession, model):
        self._session = session
        self._model = model

    async def create_note(self, note: EmptyNote, owner_uuid, todo_id: TodoID):
        stmt = insert(self._model).values(
            asdict(note),
            owner_uuid=owner_uuid,
            todo_id_fk=todo_id
        ).returning(self._model)
        result = await self._session.execute(stmt)
        await self._session.flush()

        result = result.fetchone()
        return result
