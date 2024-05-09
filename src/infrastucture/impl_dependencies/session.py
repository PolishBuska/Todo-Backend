from main.config import get_config

from infrastucture.database import Database


async def session_factory():
    config = get_config()
    db = Database(config)
    async with db.session_factory() as session:
        yield session
