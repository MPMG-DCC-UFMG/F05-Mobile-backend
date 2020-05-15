from pydantic import BaseModel
from src.application.publicwork.database.publicWorkDB import PublicWorkDB
from src.application.core.helpers import is_valid_uuid

from src.application.address.models.address import Address


class PublicWork(BaseModel):
    id: str = None
    name: str
    type_work_flag: int
    address: Address

    class Config:
        orm_mode = True

    def to_db(self) -> PublicWorkDB:
        public_work_db = PublicWorkDB(
            name=self.name,
            type_work_flag=self.type_work_flag,
            address_id=self.address.id
        )

        if id and is_valid_uuid(id):
            public_work_db.id = self.id

        return public_work_db
