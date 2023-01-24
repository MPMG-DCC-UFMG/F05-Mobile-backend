from typing import List, Optional

from pydantic import BaseModel

from application.photo.models.photo import Photo


class Collect(BaseModel):
    id: str = None
    public_work_id: str
    inspection_flag: Optional[str]
    queue_status: int = 0
    queue_status_date: int = None
    date: int
    user_email: str
    comments: str = None
    public_work_status: int = None
    photos: List[Photo] = []
    secret: bool = False

    class Config:
        orm_mode = True
