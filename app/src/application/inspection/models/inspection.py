from typing import List

from pydantic import BaseModel


class Inspection(BaseModel):
    flag: int = None
    name: str
    inquiry_number: int
    description: str
    public_work_id: str = None
    collect_id: str = None
    status: int
    user_email: str
    request_date: int = None
    secret: bool = False

    class Config:
        orm_mode = True


class InspectionDiff(BaseModel):
    operation: int
    flag: int
    name: str = None
    inquiry_number: int
    description: str = None
    public_work_id: str = None
    collect_id: str = None
    status: int = 0
    user_email: str = None
    request_date: int = None
