from pydantic import BaseModel


class Message(BaseModel):
    id: str
    sender_email: str
    reciever_email: str
    text: str
    timestamp: int
    call_id: str

    class Config:
        orm_mode = True
