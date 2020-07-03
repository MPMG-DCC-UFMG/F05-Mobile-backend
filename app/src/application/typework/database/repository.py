from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import transaction_class

from src.application.typework.models.typeWork import TypeWork
from src.application.typework.database.typeWorkDB import TypeWorkDB

from sqlalchemy_continuum.utils import version_class


def get_type_work(db: Session) -> list:
    return db.query(TypeWorkDB).all()


def add_type_work(db: Session, type_work: TypeWork) -> TypeWork:
    db_type_work = TypeWorkDB(name=type_work.name)
    db.add(db_type_work)
    db.commit()
    db.refresh(db_type_work)
    return db_type_work


def delete_type_work(db: Session, type_work_id: int) -> TypeWork:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work_id).first()
    if db_type_work:
        db.delete(db_type_work)
        db.commit()
    return db_type_work


def update_type_work(db: Session, type_work: TypeWork) -> TypeWork:
    db_type_work = db.query(TypeWorkDB).filter(TypeWorkDB.flag == type_work.flag).first()
    if db_type_work:
        db_type_work.update(type_work)
        db.commit()
        db.refresh(db_type_work)
        return db_type_work


def get_table_version(db: Session) -> int:
    version = version_class(TypeWorkDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    return last_changed[0].transaction_id
