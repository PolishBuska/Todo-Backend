from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from domain.exceptions import NoteAlreadyExist, NoteNotFoundError
from domain.models import EmptyNote
from domain.note_ioc_interface import INoteIoC
from domain.todo_ioc_interface import ITodoIoC
from infrastucture.stub import Stub
from presentation.web_api.schemas import TodoReturned, NoteCreated, NoteReturned

note_router = APIRouter(

)


@note_router.get('/{todo_id}/notes/{note_id}', response_model=NoteReturned)
async def get_note(
        todo_id: UUID,
        note_id: UUID,
        owner_id: UUID,
        ioc: Annotated[INoteIoC, Depends(Stub(INoteIoC))]
):
    try:
        async with ioc.get_note(todo_id=todo_id, note_id=note_id, owner_id=owner_id) as interactor:
            res = await interactor()
            return res
    except NoteNotFoundError as nfe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from nfe


@note_router.get('/{todo_id}/notes', response_model=TodoReturned)
async def get_todo_notes(
        todo_id: UUID,
        owner_id: UUID,
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))]
):
    async with ioc.get_todo_notes(todo_id=todo_id, owner_id=owner_id) as interactor:
        res = await interactor()
        return res


@note_router.post('/{todo_id}/notes')
async def create_note(
        note: NoteCreated,
        todo_id: UUID,
        owner_id: UUID,
        ioc: Annotated[INoteIoC, Depends(Stub(INoteIoC))]
):
    try:
        note = EmptyNote(**note.model_dump())
        async with ioc.create_note(todo_id=todo_id, owner_id=owner_id, note=note) as interactor:
            res = await interactor()
            return res
    except NoteAlreadyExist as nae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This note already exist") from nae


