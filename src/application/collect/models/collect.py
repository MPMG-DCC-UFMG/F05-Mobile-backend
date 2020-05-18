from pydantic import BaseModel

from src.application.collect.database.collectDB import CollectDB
from src.application.core.helpers import is_valid_uuid


class Collect(BaseModel):
    id: str = None
    public_work_id: str
    date: int
    comments: str = None

    class Config:
        orm_mode = True

    def to_db(self) -> CollectDB:
        collect_db = CollectDB(
            date=self.date,
            comments=self.comments,
            public_work_id=self.public_work_id
        )

        if id and is_valid_uuid(id):
            collect_db.id = self.id

        return collect_db
