from pydantic import BaseModel
from typing import List


class Inspection(BaseModel):
    flag: int = None
    name: str
    description: str
    public_work_id: str = None
    collect_id: str = None
    status: int
    user_id: str

    class Config:
        orm_mode = True
