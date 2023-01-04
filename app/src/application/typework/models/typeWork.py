from pydantic import BaseModel
from typing import List


class TypeWork(BaseModel):
    flag: int = None
    name: str
    status_list: List[int]

    class Config:
        orm_mode = True
