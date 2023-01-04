from pydantic import BaseModel


class Call(BaseModel):
    id: str
    admin_email: str
    user_email: str
    title: str
    created_at: int
    finished: bool

    class Config:
        orm_mode = True
