from typing import Optional

from application.security.models.roles import UserRoles
from pydantic import BaseModel


class User(BaseModel):
    email: str
    authentication: str
    full_name: Optional[str] = None
    picture: Optional[str] = None
    role: str = UserRoles.NORMAL.name
    anonymous: bool = False

    class Config:
        orm_mode = True
