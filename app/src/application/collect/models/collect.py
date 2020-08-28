from pydantic import BaseModel


class Collect(BaseModel):
    id: str = None
    public_work_id: str
    date: int
    user_email: str
    comments: str = None
    public_work_status: int = None

    class Config:
        orm_mode = True
