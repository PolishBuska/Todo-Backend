from uuid import UUID

from sqlalchemy import insert, select, Select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import EmptyTodo
from domain.exceptions import TodoIntegrityError
from domain.models import Todo


class TodoGateway:
    def __init__(self, model, uow: AsyncSession):
        self._model = model
        self._uow = uow

    async def create_todo(self, todo: EmptyTodo, owner_uuid) -> Todo:
        try:
            stmt = insert(self._model).values(
                name=todo.name,
                desc=todo.desc,
                owner_id=owner_uuid
            ).returning(self._model)
            res = await self._uow.execute(stmt)
            res = res.scalar()
            await self._uow.commit()
            return Todo(**res.to_dict())
        except IntegrityError as ie:
            raise TodoIntegrityError from ie

    async def get_todo(self, todo_id: UUID, owner_id: UUID) -> Todo:
        query = select(self._model).where((self._model.todo_id == todo_id) & (self._model.owner_id == owner_id))
        res = await self._uow.scalar(query)
        if not res:
            raise NoResultFound
        return Todo(**res.to_dict())
