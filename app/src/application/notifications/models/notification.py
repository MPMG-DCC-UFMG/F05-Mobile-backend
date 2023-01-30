import json

from application.notifications.models.comments import Comments
from pydantic import BaseModel


class Notification(BaseModel):
    id: str = None
    title: str
    inspection_id: str
    content: str
    user_email: str
    chat_close: bool
    answer: bool
    timestamp: int = None

    class Config:
        orm_mode = True


class PushNotification(BaseModel):
    to: str
    sound: str
    title: str
    body: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
