import uvicorn
from fastapi import FastAPI

from domain.todo_interactor_interface import ITodoInteractor
from presentation.web_api.main import main_router_factory

from src.infrastucture.impl_dependencies.create_todo import todo_interactor_factory

from src.main.config import get_config


async def app_factory() -> FastAPI:
    app = FastAPI(
        title='Todo api',
        version='1.0'
    )
    app.include_router(
        main_router_factory(
            prefix='/api/v1'
        )
    )

    return app


async def start_server(app: FastAPI) -> None:

    config = uvicorn.Config(
            app,
            host='localhost',
            port=8000,
            reload=True,
        )
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    config = get_config()
    app = await app_factory()
    app.dependency_overrides[ITodoInteractor] = todo_interactor_factory

    await start_server(app)

