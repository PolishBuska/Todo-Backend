from fastapi import Depends

from infrastucture.gateways.note_gateway import NoteGateway
from infrastucture.database import session_factory
from infrastucture.models import Note

from application.ioc.note import CNoteIoC
from application.common.uow import Commiter


async def note_ioc_factory(session=Depends(session_factory)):
    return CNoteIoC(
        note_db_gateway=(
            NoteGateway(
                session=session,
                model=Note
            )
        ),
        commiter=Commiter(
            session=session
        )
    )
