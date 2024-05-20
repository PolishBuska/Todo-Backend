from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query

from domain.exceptions import NoteAlreadyExist, NoteNotFoundError, NoteNotFoundByPk, TodoNotFoundByPk
from domain.models import EmptyNote, TodoNotesStatusDTO
from domain.note_ioc_interface import INoteIoC
from domain.todo_ioc_interface import ITodoIoC
from infrastucture.stub import Stub
from presentation.web_api.schemas import TodoReturned, NoteCreated, NoteReturned, TodoNotesStatus, Status

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
        owner_id: UUID,
        todo_notes_data: Annotated[Query, Depends(TodoNotesStatus)],
        ioc: Annotated[ITodoIoC, Depends(Stub(ITodoIoC))]
):
    try:
        if todo_notes_data.select_status == Status.confirmed:
            data = TodoNotesStatusDTO(
                todo_id=todo_notes_data.todo_id,
                select_status=True
            )
        else:
            data = TodoNotesStatusDTO(
                todo_id=todo_notes_data.todo_id,
                select_status=False
            )

        async with ioc.get_todo_notes(todo_notes_query_dto=data, owner_id=owner_id) as interactor:
            res = await interactor()
            return res
    except TodoNotFoundByPk as tnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'message': 'This todo does not exist',
                'reason': 'We could not find it',
                'solutions': 'Check if it exists'
            }
        ) from tnf


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


@note_router.put('/{todo_id}/notes/{note_id}')
async def update_note(
        ioc: Annotated[INoteIoC, Depends(Stub(INoteIoC))],
        note: NoteCreated,
        todo_id: UUID,
        note_id: UUID,
        owner_id: UUID
):
    note = EmptyNote(**note.model_dump())
    try:
        async with ioc.update_note(
                todo_id=todo_id,
                note_id=note_id,
                owner_id=owner_id,
                note=note
        ) as interactor:
            res = await interactor()
            return res
    except NoteNotFoundByPk as nnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from nnf


@note_router.delete('/{todo_id}/notes/{note_id}')
async def delete_note(
        ioc: Annotated[INoteIoC, Depends(Stub(INoteIoC))],
        note_id: UUID,
        todo_id: UUID,
        owner_id: UUID
):
    try:
        async with ioc.delete_note(
            owner_id=owner_id,
            todo_id=todo_id,
            note_id=note_id
        ) as interactor:
            res = await interactor()
            return res
    except NoteNotFoundByPk as nnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found') from nnf
