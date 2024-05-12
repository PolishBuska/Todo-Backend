from typing import List
from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload, noload
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import EmptyTodo
from domain.exceptions import TodoIntegrityError, TodoNotFoundError
from domain.models import Todo, DeletedResult


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
            ).options(noload(self._model.notes)).returning(self._model)
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
            raise TodoNotFoundError
        return Todo(**res.to_dict())

    async def get_todo_notes(self, todo_id: UUID, owner_id: UUID) -> Todo:
        query = select(self._model).options(
            selectinload(self._model.notes)
        ).where((self._model.todo_id == todo_id) & (self._model.owner_id == owner_id))
        res = await self._uow.scalar(query)

        return Todo(**res.to_dict())

    async def get_todos_owner(self, owner_id: UUID) -> List[Todo]:
        query = select(self._model).options(noload(self._model.notes)).where(self._model.owner_id == owner_id)
        res = await self._uow.scalars(query)

        res = [(Todo(**todo.to_dict())) for todo in res.all()]
        return res

    async def update_todo(self, todo: EmptyTodo, todo_id: UUID, owner_id: UUID) -> Todo:
        stmt = update(self._model).values(
            name=todo.name,
            desc=todo.desc
        ).options(noload(self._model.notes)).where(
            (self._model.todo_id == todo_id) & (self._model.owner_id == owner_id)
        ).returning(self._model)
        res = await self._uow.execute(stmt)
        res = res.scalar()
        if not res:
            raise TodoNotFoundError
        await self._uow.commit()
        return Todo(**res.to_dict())

    async def delete_todo(self, todo_id: UUID, owner_id: UUID):
        stmt = delete(self._model).where(
            (self._model.todo_id == todo_id) & (self._model.owner_id == owner_id)
        ).returning(self._model.todo_id)
        res = await self._uow.execute(stmt)
        res = res.scalar()
        if not res:
            raise TodoNotFoundError
        await self._uow.commit()
        return DeletedResult(
            item_id=res,
            success=True
        )
