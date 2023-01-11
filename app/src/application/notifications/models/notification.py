from pydantic import BaseModel

from application.notifications.models.comments import Comments


class Notification(BaseModel):
    id: str
    title: str
    inspection_id: str
    content: str
    user_email: str
    timestamp: int

    class Config:
        orm_mode = True
