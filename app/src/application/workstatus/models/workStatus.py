from typing import List

from pydantic import BaseModel


class WorkStatus(BaseModel):
    flag: int = None
    name: str
    description: str
    type_work_list: List[int] = []

    class Config:
        orm_mode = True
