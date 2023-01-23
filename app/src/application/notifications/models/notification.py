from application.notifications.models.comments import Comments
from pydantic import BaseModel


class Notification(BaseModel):
    id: str = None
    title: str
    inspection_id: str
    content: str
    user_email: str
    answer: bool
    timestamp: int = None

    class Config:
        orm_mode = True
