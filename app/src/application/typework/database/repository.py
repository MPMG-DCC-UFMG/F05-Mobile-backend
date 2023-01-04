from typing import List

from application.typephoto.database.typePhotoDB import TypePhotoDB
from application.workstatus.database.workStatusDB import WorkStatusDB
from sqlalchemy import desc
from sqlalchemy.orm import Session

from application.typework.models.typeWork import TypeWork
from application.typework.database.typeWorkDB import TypeWorkDB

from sqlalchemy_continuum.utils import version_class


def get_type_work(db: Session) -> list:
    db_type_works = db.query(TypeWorkDB).all()
    return list(map(lambda type_work: type_work.parse_to_type_work(), db_type_works))


def get_type_work_type_photos(db: Session, type_work_id: int) -> list:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    return db_type_work.type_photos


def get_type_work_work_status(db: Session, type_work_id: int) -> list:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    return db_type_work.work_statuses


def add_type_work(db: Session, type_work: TypeWork) -> TypeWork:
    db_type_work = TypeWorkDB.from_model(type_work)
    db.add(db_type_work)
    db.commit()
    db.refresh(db_type_work)
    return db_type_work.parse_to_type_work()


def delete_type_work(db: Session, type_work_id: int) -> TypeWork:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    if db_type_work:
        db.delete(db_type_work)
        db.commit()
    return db_type_work.parse_to_type_work()


def update_type_work(db: Session, type_work: TypeWork) -> TypeWork:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work.flag).first()
    if db_type_work:
        db_type_work.update(type_work)
        db.commit()
        db.refresh(db_type_work)
        return db_type_work.parse_to_type_work()


def get_table_version(db: Session) -> int:
    version = version_class(TypeWorkDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1


def add_type_photo_to_type_work(db: Session, type_work_id: int, type_photo_id: int) -> bool:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    db_type_photo = db.query(TypePhotoDB).filter(TypePhotoDB.flag == type_photo_id).first()
    if db_type_work and db_type_photo:
        db_type_work.type_photos.append(db_type_photo)
        db.commit()
        db.refresh(db_type_work)
        return True
    else:
        return False


def update_type_photos_to_type_work(db: Session, type_work_id: int, type_photos: List[int]) -> bool:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    db_type_photos = db.query(TypePhotoDB).filter(TypePhotoDB.flag.in_(type_photos))
    if db_type_work and db_type_photos.count() > 0:
        db_type_work.type_photos = []
        db.commit()
        for type_photo in list(db_type_photos):
            db_type_work.type_photos.append(type_photo)
        db.commit()
        db.refresh(db_type_work)
        return True
    else:
        return False


def update_work_statuses_of_type_work(db: Session, type_work_id: int, work_statuses: List[int]) -> bool:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    db_work_statuses = db.query(WorkStatusDB).filter(WorkStatusDB.flag.in_(work_statuses))
    if db_type_work and db_work_statuses.count() > 0:
        db_type_work.work_statuses = []
        db.commit()
        for work_status in list(db_work_statuses):
            db_type_work.work_statuses.append(work_status)
        db.commit()
        db.refresh(db_type_work)
        return True
    else:
        return False
