from fastapi.routing import APIRouter
from app.api.main_api import any_api

api_router = APIRouter()

api_router.include_router(any_api, tags=['any_tag'], prefix='')
