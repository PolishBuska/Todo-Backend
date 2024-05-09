from fastapi import Depends

from infrastucture.gateways.note_gateway import NoteGateway
from infrastucture.database import session_factory

from application.ioc.note import CNoteIoC


async def note_ioc_factory(session=Depends(session_factory)):
    return CNoteIoC(
        (
            NoteGateway(
                session=session,
                model=None
            )
        )
    )
