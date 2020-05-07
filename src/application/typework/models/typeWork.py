from pydantic import BaseModel


class TypeWork(BaseModel):
    name: str
    flag: int
