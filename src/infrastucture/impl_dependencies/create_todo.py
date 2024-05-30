from fastapi import Depends

from src.infrastucture.gateways.todo_gateway import TodoGateway
from src.infrastucture.models import Todo
from src.infrastucture.database import session_factory

from src.application.ioc.todo import CTodoIoC


async def todo_ioc_factory(session=Depends(session_factory)):
    return CTodoIoC(
        (
            TodoGateway(
                model=Todo,
                uow=session
            )
        )
    )
