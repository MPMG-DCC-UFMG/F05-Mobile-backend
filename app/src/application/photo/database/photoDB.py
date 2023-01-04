from sqlalchemy import Column, Float, String, BigInteger, ForeignKey

from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.photo.models.photo import Photo

class PhotoDB(Base):
    __tablename__ = "photo"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    filepath = Column(String)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    comment = Column(String)
    timestamp = Column(BigInteger)

    collect_id = Column(String, ForeignKey("collect.id"))

    @classmethod
    def from_model(cls, photo: Photo):
        photo_db = PhotoDB(
            type=photo.type,
            collect_id=photo.collect_id,
            comment=photo.comment,
            filepath=photo.filepath,
            longitude=photo.longitude,
            latitude=photo.latitude,
            timestamp=photo.timestamp
        )

        if photo.id and is_valid_uuid(photo.id):
            photo_db.id = photo.id

        return photo_db
