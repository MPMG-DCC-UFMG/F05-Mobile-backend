from pydantic import BaseModel


class TypePhoto(BaseModel):
    name: str
    flag: int = None
    description: str = None

    class Config:
        orm_mode = True
