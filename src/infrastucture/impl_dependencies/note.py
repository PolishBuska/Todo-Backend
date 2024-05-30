from fastapi import Depends

from src.infrastucture.gateways.note_gateway import NoteGateway
from src.infrastucture.database import session_factory
from src.infrastucture.models import Note

from src.application.ioc.note import CNoteIoC
from src.application.common.uow import Commiter


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
