from fastapi import Depends

from infrastucture.gateways.todo_gateway import TodoGateway
from infrastucture.models import Todo
from infrastucture.database import session_factory

from application.ioc.todo import CTodoIoC


async def todo_ioc_factory(session=Depends(session_factory)):
    return CTodoIoC(
        (
            TodoGateway(
                model=Todo,
                uow=session
            )
        )
    )
