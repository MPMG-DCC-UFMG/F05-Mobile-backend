from pydantic import BaseModel

from application.address.models.address import Address


class PublicWork(BaseModel):
    id: str = None
    name: str
    type_work_flag: int
    address: Address
    user_status: int = None
    queue_status: int = 0
    queue_status_date: int = None
    rnn_status: int = None
    profile_picture: str = None

    class Config:
        orm_mode = True


class PublicWorkDiff(BaseModel):
    operation: int
    id: str
    name: str = None
    type_work_flag: int = None
    address: Address = None
    user_status: int = 0
    queue_status: int = 0
    queue_status_date: int = None
    profile_picture: str = None
