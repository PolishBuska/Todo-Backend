from fastapi import Depends

from infrastucture.impl_dependencies.session import session_factory
from infrastucture.gateways.todo_gateway import TodoGateway

from application.ioc.todo import CTodoIoC


async def todo_interactor_factory():
    return CTodoIoC(
        (
            TodoGateway(
                session=Depends(session_factory),
                model=None
            )
        )
    )
