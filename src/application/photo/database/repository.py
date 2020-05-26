from typing import List

from sqlalchemy.orm import Session

from src.application.photo.database.photoDB import PhotoDB
from src.application.photo.models.photo import Photo


def get_all_photos(db: Session) -> List[Photo]:
    return db.query(PhotoDB).all()


def add_photo(db: Session, photo: Photo) -> Photo:
    db_photo = photo.to_db()
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo
