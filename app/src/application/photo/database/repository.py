from typing import List

from sqlalchemy.orm import Session

from src.application.photo.database.photoDB import PhotoDB
from src.application.photo.models.photo import Photo


def get_all_photos(db: Session) -> List[Photo]:
    return db.query(PhotoDB).all()


def get_photos_by_collect_id(db: Session, collect_id: str) -> List[Photo]:
    return db.query(PhotoDB).filter(PhotoDB.collect_id == collect_id).all()


def add_photo(db: Session, photo: Photo) -> Photo:
    db_photo = PhotoDB.from_model(photo)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo
