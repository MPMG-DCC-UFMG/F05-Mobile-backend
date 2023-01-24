from typing import List

from pydantic import BaseModel
from application.photo.models.photo import Photo


class CollectReport(BaseModel):
    id: str = None
    public_work_id: str
    inspection_flag: str
    date: int
    user_email: str
    comments: str = None
    public_work_status: int = None
    photos: List[Photo]
    secret: bool = False

    class Config:
        orm_mode = True
