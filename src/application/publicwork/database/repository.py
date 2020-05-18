from sqlalchemy.orm import Session
from sqlalchemy_continuum import transaction_class

from src.application.publicwork.models.publicwork import PublicWork
from src.application.publicwork.database.publicWorkDB import PublicWorkDB


def get_public_work(db: Session) -> list:
    public_work_list = db.query(PublicWorkDB).all()
    return public_work_list


def get_table_version(db: Session) -> int:
    transaction = transaction_class(PublicWorkDB)
    return db.query(transaction).count()


def add_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = public_work.to_db()
    db.add(db_public_work)
    db.commit()
    db.refresh(db_public_work)
    return db_public_work


def delete_public_work(db: Session, public_work_id: str) -> PublicWork:
    db_public_work = db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work_id).first()
    if db_public_work:
        db.delete(db_public_work)
        db.commit()
    return db_public_work


def update_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work.id).first()
    if db_public_work:
        db_public_work = public_work.to_db()
        db.commit()
        db.refresh(db_public_work)
        return db_public_work
