from pydantic import BaseModel


class AnySchema(BaseModel):
    name: str
