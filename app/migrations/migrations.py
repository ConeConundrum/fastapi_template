from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from alembic import command, config

from app.settings.config import config as app_config
from app.settings.logging import logger
from app.database.database import get_db_url


async def run_async_upgrade() -> None:
    def __run_upgrade(connection, cfg):
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    logger.warning('Run database auto migrations')
    async_engine: AsyncEngine = create_async_engine(
        get_db_url(),
        echo=True if app_config.TEST else False
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(__run_upgrade, config.Config("alembic.ini"))
    logger.warning('Database auto migrations complete')


async def run_async_downgrade() -> None:
    def __run_downgrade(connection, cfg):
        cfg.attributes["connection"] = connection
        command.downgrade(cfg, "base")

    logger.warning('Run database downgrade')
    async_engine: AsyncEngine = create_async_engine(
        get_db_url(),
        echo=True if app_config.TEST else False
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(__run_downgrade, config.Config('alembic.ini'))
    logger.warning('Database downgrade complete')
