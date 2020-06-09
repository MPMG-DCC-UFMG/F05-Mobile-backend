from pydantic import BaseModel


class TypePhoto(BaseModel):
    name: str
    flag: int = None

    class Config:
        orm_mode = True
