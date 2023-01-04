from pydantic import BaseModel


class Photo(BaseModel):
    id: str
    collect_id: str
    type: str
    filepath: str
    latitude: float
    longitude: float
    comment: str = None
    timestamp: int

    class Config:
        orm_mode = True
