from typing import List

from application.photo.models.photo import Photo
from pydantic import BaseModel


class Collect(BaseModel):
    id: str = None
    public_work_id: str
    inspection_flag: str
    queue_status: int = 0
    queue_status_date: int = None
    date: int
    user_email: str
    comments: str = None
    public_work_status: int = None
    photos: List[Photo] = []

    class Config:
        orm_mode = True
