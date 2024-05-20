from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from main.config import Settings, get_config


class Database:
    def __init__(self, config: Settings):
        self._config = config
        self._engine = create_async_engine(url=self._config.db_url, echo=False)

    @property
    def engine(self):
        return self._engine


def db_factory(config):
    return Database(config)


async def session_factory() -> AsyncContextManager[AsyncSession]:
    _config = get_config()
    _db = db_factory(_config)
    _engine = _db.engine
    _session = async_sessionmaker(_engine, expire_on_commit=False)
    async with _session() as session:
        yield session


def get_base():
    _base = declarative_base()
    return _base
