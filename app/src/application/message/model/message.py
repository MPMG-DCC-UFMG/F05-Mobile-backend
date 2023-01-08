from pydantic import BaseModel


class Message(BaseModel):
    id: str = None
    sender_email: str
    receiver_email: str
    text: str
    timestamp: int = None
    call_id: str
    readed: bool = None

    class Config:
        orm_mode = True
