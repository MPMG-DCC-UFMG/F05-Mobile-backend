from pydantic import BaseModel


class Call(BaseModel):
    id: str = None
    admin_email: str
    user_email: str
    title: str
    created_at: int = None
    closed: bool = None
    closed_at: int = None

    class Config:
        orm_mode = True
