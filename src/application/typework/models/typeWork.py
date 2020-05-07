from pydantic import BaseModel


class TypeWork(BaseModel):
    name: str
    flag: int = None

    class Config:
        orm_mode = True
