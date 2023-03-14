from fastapi import FastAPI

from app.api.api import api_router
from app.database.database import initiate_db, get_sqlalchemy_engine
from app.migrations.migrations import run_async_upgrade, run_async_downgrade
from app.settings.config import config
from app.settings.logging import logger


app = FastAPI(title=config.SERVICE_NAME, version=config.VERSION)
app.include_router(api_router)


@app.on_event("startup")
async def db_setup_at_startup():
    logger.warning(f"Startup server with TEST {config.TEST} and AUTO MIGRATIONS {config.AUTO_MIGRATIONS}")

    await initiate_db()
    app.state.alchemy_engine = await get_sqlalchemy_engine()

    if config.AUTO_MIGRATIONS:
        await run_async_upgrade()

    logger.info("Service startup complete")


@app.on_event("shutdown")
async def db_close_at_shutdown():
    logger.warning("Shutdown server")
    if app.state.alchemy_engine:
        await app.state.alchemy_engine.dispose()

    if config.TEST:
        await run_async_downgrade()

    logger.info("Service shutdown complete")
