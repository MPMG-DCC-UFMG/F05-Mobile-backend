from pydantic import BaseModel


class Comments(BaseModel):
    id: str
    notification_id: str
    content: str
    user_email: str
    timestamp: int
