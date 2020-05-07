from sqlalchemy.orm import Session

from src.application.typework.models.typeWork import TypeWork
from src.application.typework.database.typeWorkDB import TypeWorkDB


def get_type_work(db: Session) -> list:
    return db.query(TypeWorkDB).all()


def add_type_work(db: Session, type_work: TypeWork):
    db_type_work = TypeWorkDB(name=type_work.name)
    db.add(db_type_work)
    db.commit()
    db.refresh(db_type_work)
    return db_type_work
