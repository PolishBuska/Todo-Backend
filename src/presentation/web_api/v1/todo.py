from typing import Annotated

from fastapi import APIRouter, Depends

from domain.models import EmptyTodo
from domain.todo_interactor_interface import ITodoInteractor
from infrastucture.stub import Stub
from presentation.web_api.schemas import TodoCreated

todo_router = APIRouter(

)


@todo_router.post('/')
async def create_todo(
        todo: TodoCreated,
        owner_id: int,
        ioc: Annotated[ITodoInteractor,
        Depends(Stub(ITodoInteractor))]
                      ):
    todo = EmptyTodo(**todo.model_dump())
    async with ioc.create_todo(todo=todo, owner_uuid=owner_id) as interactor:
        res = await interactor()
        return res
