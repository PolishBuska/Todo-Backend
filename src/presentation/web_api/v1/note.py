from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from domain.models import EmptyNote
from domain.note_ioc_interface import INoteIoC
from infrastucture.stub import Stub
from presentation.web_api.schemas import NoteCreated

note_router = APIRouter(

)


@note_router.post('/{todo_id}')
async def create_note(
        note: NoteCreated,
        todo_id: UUID,
        owner_id: UUID,
        ioc: Annotated[INoteIoC, Depends(Stub(INoteIoC))]
):
    note = EmptyNote(**note.model_dump())
    async with ioc.create_note(todo_id=todo_id, owner_uuid=owner_id, note=note) as interactor:
        res = await interactor()
        return res
