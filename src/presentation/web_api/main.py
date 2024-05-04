from fastapi import APIRouter

from src.presentation.web_api.v1.todo import todo_router


def main_router_factory(prefix):
    main_router = APIRouter(
        prefix=prefix
    )
    main_router.include_router(
        todo_router,
        prefix='/todo',
        tags=['todo']
    )
    return main_router

