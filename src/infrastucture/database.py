
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.main.config import Settings


class Database:
    def __init__(self, config: Settings):
        self._config = config
        self._engine = create_async_engine(url=self._config.db_url)

    @property
    def engine(self):
        return self._engine

    def session_factory(self) -> AsyncSession:
        _engine = self._engine
        _session = async_sessionmaker(_engine, expire_on_commit=False)
        return _session()


def db_factory(config):
    return Database(config)


def get_base():
    _base = declarative_base()
    return _base
