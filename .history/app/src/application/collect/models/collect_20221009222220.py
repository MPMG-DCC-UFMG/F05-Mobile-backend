from typing import List

from application.photo.models.photo import Photo
from pydantic import BaseModel


class Collect(BaseModel):
    id: str = None
    public_work_id: str
    inspection_flag: str
    date: int
    user_email: str
    comments: str = None
    public_work_status: int = None
    photos: List[Photo] = []

    class Config:
        orm_mode = True
