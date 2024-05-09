from fastapi import APIRouter

from src.presentation.web_api.v1.todo import todo_router
from src.presentation.web_api.v1.note import note_router


def main_router_factory(prefix):
    main_router = APIRouter(
        prefix=prefix
    )
    main_router.include_router(
        todo_router,
        prefix='/todos',
        tags=['todo']
    )
    main_router.include_router(
        note_router,
        prefix='/notes',
        tags=['notes']
    )
    return main_router

