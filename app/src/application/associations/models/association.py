from pydantic import BaseModel


class AssociationTypePhPW(BaseModel):
    type_work_flag: int
    type_photo_flag: int

    class Config:
        orm_mode = True
