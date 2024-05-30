from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.exceptions import TodoAlreadyExist, TodoNotFoundByPk, TodoNotesEmptyError, TodoNotesStatusFalse
from src.domain.models import EmptyTodo
from src.presentation.todo_ioc_interface import ITodoIoC

from src.infrastucture.stub import Stub

from src.presentation.web_api.schemas import TodoCreated, TodoReturned, TodoDeleted, ListTodoReturned

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
    try:
        async with ioc.get_todo(owner_id=owner_id, todo_id=todo_id) as interactor:
            result = await interactor()
            return result
    except TodoNotFoundByPk as tnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        ) from tnf


@todo_router.put('/{todo_id}', response_model=TodoReturned)
async def update_todo(
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))],
        todo: TodoCreated,
        todo_id: UUID,
        owner_id: UUID
):
    try:
        todo = EmptyTodo(**todo.model_dump())
        async with ioc.update_todo(todo=todo, todo_id=todo_id, owner_id=owner_id) as interactor:
            res = await interactor()
            return res
    except TodoNotFoundByPk as tnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from tnf


@todo_router.get('/', response_model=ListTodoReturned)
async def get_todos_owner(
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))],
        owner_id: UUID
):
    try:
        async with ioc.get_todos_owner(owner_id) as interactor:
            res = await interactor()
            res = ListTodoReturned(todos=res)
            return res
    except TodoNotFoundByPk as tnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from tnf


@todo_router.delete('/{todo_id}', response_model=TodoDeleted)
async def delete_todo(
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))],
        owner_id: UUID,
        todo_id: UUID
):
    try:
        async with ioc.delete_todo(todo_id=todo_id, owner_id=owner_id) as interactor:
            res = await interactor()
            return res
    except TodoNotFoundByPk as tnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from tnf


@todo_router.post('/{todo_id}')
async def confirm_todo(
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))],
        todo_id: UUID,
        owner_id: UUID
):
    try:
        async with ioc.confirm_todo(todo_id=todo_id, owner_id=owner_id) as interactor:
            res = await interactor()
            return res
    except TodoNotesEmptyError as tne:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Cannot confirm todo',
                'reason': 'Todo is empty',
                'solutions': 'Add at least one note to todo'
            }
        ) from tne
    except TodoNotesStatusFalse as tns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Cannot confirm todo',
                'reason': 'All notes must be confirmed first',
                'solutions': 'Confirm all notes'
            }
        ) from tns

