from fastapi import APIRouter

from src.presentation.web_api.v1.authenticated_router import authenticated_router_factory
from src.presentation.web_api.v1.resources.todo import todo_router
from src.presentation.web_api.v1.resources.note import note_router


def main_router_factory(prefix):

    authenticated_router = authenticated_router_factory(
        prefix='/me',
    )

    authenticated_router.include_router(
        todo_router,
        prefix='/todos',
        tags=['todos']
    )
    authenticated_router.include_router(
        note_router,
        prefix='/todos',
        tags=['notes']
    )

    main_router = APIRouter(
        prefix=prefix
    )

    main_router.include_router(
        authenticated_router
    )

    return main_router

