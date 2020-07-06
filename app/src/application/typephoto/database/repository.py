from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import transaction_class, version_class

from src.application.typephoto.models.typePhoto import TypePhoto
from src.application.typephoto.database.typePhotoDB import TypePhotoDB


def get_type_photo(db: Session) -> list:
    return db.query(TypePhotoDB).all()


def add_type_photo(db: Session, type_photo: TypePhoto) -> TypePhoto:
    db_type_photo = TypePhotoDB(name=type_photo.name)
    db.add(db_type_photo)
    db.commit()
    db.refresh(db_type_photo)
    return db_type_photo


def delete_type_photo(db: Session, type_photo_id: int) -> TypePhoto:
    db_type_photo = db.query(TypePhotoDB).filter(TypePhotoDB.flag == type_photo_id).first()
    if db_type_photo:
        db.delete(db_type_photo)
        db.commit()
    return db_type_photo


def update_type_photo(db: Session, type_photo: TypePhoto) -> TypePhoto:
    db_type_photo = db.query(TypePhotoDB).filter(TypePhotoDB.flag == type_photo.flag).first()
    if db_type_photo:
        db_type_photo.update(type_photo)
        db.commit()
        db.refresh(db_type_photo)
        return db_type_photo


def get_table_version(db: Session) -> int:
    version = version_class(TypePhotoDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    return last_changed[0].transaction_id
