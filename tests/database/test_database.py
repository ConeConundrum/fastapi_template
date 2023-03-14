import pytest

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from app.database.database import get_sqlalchemy_engine


def test_get_states(client):
    assert client.app.state.alchemy_engine
    assert isinstance(client.app.state.alchemy_engine, AsyncEngine)


@pytest.mark.asyncio
async def test_get_sqlalchemy_engine():
    engine = await get_sqlalchemy_engine()
    assert engine
    assert isinstance(engine, AsyncEngine)

    async with engine.connect() as connection:
        result = await connection.execute(text('SELECT 1;'))
    assert result


@pytest.mark.asyncio
async def test_check_app_alchemy_engine(client):
    assert client.app.state.alchemy_engine

    async with client.app.state.alchemy_engine.connect() as connection:
        result = await connection.execute(text('SELECT 1;'))
    assert result


@pytest.mark.asyncio
async def test_database_initialized(client):
    assert client.app.state.alchemy_engine

    async with client.app.state.alchemy_engine.connect() as connection:
        result = await connection.execute(text('SELECT * FROM users'))
    assert result

