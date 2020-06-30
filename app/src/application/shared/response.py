from pydantic.main import BaseModel


class Error(BaseModel):
    status_code: int
    message: str


class Response(BaseModel):
    success: bool
    error: Error = None
