
from fastapi import APIRouter


def authenticated_router_factory(prefix: str):

    authenticated_router = APIRouter(
        prefix=prefix,
    )

    return authenticated_router

