from pydantic import BaseModel

from src.application.address.models.address import Address


class PublicWork(BaseModel):
    id: str = None
    name: str
    type_work_flag: int
    address: Address

    class Config:
        orm_mode = True


class PublicWorkDiff(PublicWork):
    operation: int
