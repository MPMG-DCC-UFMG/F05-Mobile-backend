from pydantic import BaseModel

from src.application.photo.database.photoDB import PhotoDB
from src.application.core.helpers import is_valid_uuid


class Photo(BaseModel):
    id: str
    type: str
    filepath: str
    latitude: float
    longitude: float
    comment: str = None
    timestamp: int

    class Config:
        orm_mode = True

    def to_db(self) -> PhotoDB:
        photo_db = PhotoDB(
            type=self.type,
            comment=self.comment,
            filepath=self.filepath,
            longitude=self.longitude,
            latitude=self.latitude,
            timestamp=self.timestamp
        )

        if id and is_valid_uuid(id):
            photo_db.id = self.id

        return photo_db
