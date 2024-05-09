from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from domain.models import EmptyTodo


class TodoGateway:
    def __init__(self, session: AsyncSession, model):
        self._session = session
        self._model = model

    async def create_todo(self, todo: EmptyTodo, owner_uuid):
        stmt = insert(self._model).values(asdict(todo), owner_uuid=owner_uuid).returning(self._model)
        result = await self._session.execute(stmt)
        await self._session.flush()

        result = result.fetchone()
        return result
