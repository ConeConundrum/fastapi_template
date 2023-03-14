from fastapi import APIRouter, status
from app.settings.logging import logger


any_api = APIRouter()


@any_api.get('/', status_code=status.HTTP_200_OK, response_model=str)
async def home() -> str:
    logger.info('get request')
    return 'OK'
