from httpx import AsyncClient

from src.main.web import app_factory

import pytest


@pytest.fixture
async def test_app():
    app = await app_factory()
    yield app


@pytest.fixture
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_healthcheck(test_client):

    resp = await test_client.get(
        "api/v1/health", params={'a': 1123}
    )
    assert resp.status_code == 200
    assert resp.json()["param"] == '1123'
