from enum import Enum


class HttpErrorEnum(str, Enum):
    """Str enumerate for http errors"""
    NO_DB_CONNECTION = "Database connection error"
    NO_DB_ENGINE = "Database engine create error"
