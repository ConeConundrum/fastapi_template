import asyncio
from typing import Union

import asyncpg
from sqlalchemy import NullPool, QueuePool

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import declarative_base

from app.components.http_errors import HttpErrorEnum
from app.settings.config import config
from app.settings.logging import logger


Base = declarative_base()


def get_db_url(with_driver=True, with_db_name=True):
    user = config.POSTGRES_USER
    password = config.POSTGRES_PASSWORD
    server = config.POSTGRES_SERVER
    port = config.POSTGRES_PORT
    db = config.POSTGRES_DB

    if with_driver and with_db_name:
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"
    elif with_db_name:
        return f"postgresql://{user}:{password}@{server}:{port}/{db}"
    elif with_driver:
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}"
    else:
        f"postgresql://{user}:{password}@{server}:{port}"


async def initiate_db():
    """Create db if not exist on startup and wait until successful connection"""

    logger.info('Database initialization')
    connection = None
    retries = 0

    while retries < config.POSTGRES_CONNECTION_RETRIES and not connection:
        try:
            logger.debug(
                f'Try to connect to database '
                f'{config.POSTGRES_SERVER}, '
                f'{config.POSTGRES_PORT}, '
                f'{config.POSTGRES_DB}'
            )

            connection = await asyncpg.connect(
                dsn=get_db_url(with_driver=False)
            )
            await connection.close()
            return
        except asyncpg.InvalidCatalogNameError:
            logger.warning(
                f'Database {config.POSTGRES_DB} does not exist. '
                f'\n Creating database {config.POSTGRES_DB}'
            )
            # Database does not exist, create it.
            sys_conn = await asyncpg.connect(
                dsn=get_db_url(with_driver=False)
            )
            await sys_conn.execute(
                f'CREATE DATABASE "{config.POSTGRES_DB}" OWNER "{config.POSTGRES_USER}"'
            )
            await sys_conn.close()
            logger.info(f'Successfully create database {config.POSTGRES_DB}')
            return

        except (ConnectionRefusedError, asyncpg.CannotConnectNowError):
            logger.warning('Connection refused')

        except Exception as e:
            logger.critical(f'Connection error {e.__str__()}')

        finally:
            logger.warning('Retry connection to DB')
            retries += 1
            await asyncio.sleep(1)

    raise ConnectionError(HttpErrorEnum.NO_DB_CONNECTION.value)


async def get_sqlalchemy_engine() -> AsyncEngine:
    logger.info('Database sqlalchemy engine initialization')
    retries = 0
    engine: Union[AsyncEngine, None] = None

    while retries < config.POSTGRES_CONNECTION_RETRIES and not engine:
        try:
            if config.TEST:
                engine: AsyncEngine = create_async_engine(
                    url=get_db_url(),
                    echo=True,
                    poolclass=NullPool
                )
            else:
                engine: AsyncEngine = create_async_engine(
                    url=get_db_url(),
                    echo=False,
                    poolclass=QueuePool,
                    pool_size=config.MAX_POOL_SIZE
                )

        except Exception as e:
            logger.critical(f"Sqlalchemy engine create error: {e.__str__()}")

        finally:
            retries += 1
            await asyncio.sleep(1)

    if not engine:
        raise ConnectionError(HttpErrorEnum.NO_DB_ENGINE.value)

    logger.info('Database sqlalchemy engine initialization complete')
    return engine
