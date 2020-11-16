from typing import List

from pydantic import BaseModel


class WorkStatus(BaseModel):
    flag: int = None
    name: str
    description: str

    class Config:
        orm_mode = True
