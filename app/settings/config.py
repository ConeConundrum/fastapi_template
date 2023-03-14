from pydantic import BaseSettings


class Settings(BaseSettings):
    """Microservice config"""

    VERSION: str = '1.0'
    LOG_LEVEL: str = 'INFO'
    SERVICE_NAME: str = 'BLUEPRINT'
    SERVICE_PORT: int = 80
    TEST: bool = False

    AUTO_MIGRATIONS: bool = False

    # Postgres settings
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_PORT: int = 5432
    POSTGRES_CONNECTION_RETRIES: int = 1
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5

    class Config:
        case_sensitive = True
        env_file = '.env'  # NOTE TO CHANGE IT ON PRODUCTION


config = Settings()
