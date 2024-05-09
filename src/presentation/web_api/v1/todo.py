from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from domain.exceptions import TodoAlreadyExist
from domain.models import EmptyTodo
from domain.todo_ioc_interface import ITodoIoC

from infrastucture.stub import Stub

from presentation.web_api.schemas import TodoCreated, TodoReturned

todo_router = APIRouter(

)


@todo_router.post('/', response_model=TodoReturned)
async def create_todo(
        todo: TodoCreated,
        owner_id: UUID,
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))]
):
    try:
        todo = EmptyTodo(**todo.model_dump())
        async with ioc.create_todo(todo=todo, owner_uuid=owner_id) as interactor:
            res = await interactor()
            return res
    except TodoAlreadyExist as tae:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo with such name already exists"
        ) from tae


@todo_router.get('/{todo_id}', response_model=TodoReturned)
async def get_todo(
        owner_id: UUID,
        todo_id: UUID,
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))]
):
    async with ioc.get_todo(owner_id=owner_id, todo_id=todo_id) as interactor:
        result = await interactor()
        return result
