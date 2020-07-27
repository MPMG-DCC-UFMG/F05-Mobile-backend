from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str
    authentication: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True
