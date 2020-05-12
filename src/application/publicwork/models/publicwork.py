from pydantic import BaseModel
from src.application.publicwork.database.publicWorkDB import PublicWorkDB
from src.application.core.helpers import is_valid_uuid


class PublicWork(BaseModel):
    id: str = None
    name: str
    type_work_flag: int


    class Config:
        orm_mode = True

    def to_db(self) -> PublicWorkDB:
        public_work_db = PublicWorkDB(
            name=self.name,
            type_work_flag=self.type_work_flag
        )

        if id and is_valid_uuid(id):
            public_work_db.id = self.id

        return public_work_db
