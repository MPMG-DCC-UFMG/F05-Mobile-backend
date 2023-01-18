from pydantic import BaseModel


class Comments(BaseModel):
    id: str
    notification_id: str
    content: str
    receive_email: str
    send_email: str
    timestamp: int
