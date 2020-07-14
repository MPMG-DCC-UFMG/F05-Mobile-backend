from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import version_class, Operation

from src.application.publicwork.models.publicwork import PublicWork, PublicWorkDiff
from src.application.publicwork.database.publicWorkDB import PublicWorkDB


def get_public_work(db: Session) -> list:
    return db.query(PublicWorkDB).all()


def add_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = PublicWorkDB.from_model(public_work)
    db.add(db_public_work)
    db.commit()
    db.refresh(db_public_work)
    return db_public_work


def delete_public_work(db: Session, public_work_id: str) -> PublicWork:
    db_public_work = db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work_id).first()
    if db_public_work:
        db.delete(db_public_work)
        db.delete(db_public_work.address)
        db.commit()
    return db_public_work


def update_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work.id).first()
    if db_public_work:
        db_public_work.update(public_work)
        db.commit()
        db.refresh(db_public_work)
        return db_public_work


def upsert_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = update_public_work(db, public_work)
    if db_public_work:
        return db_public_work
    else:
        return add_public_work(db, public_work)


def get_table_version(db: Session) -> int:
    version = version_class(PublicWorkDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    return last_changed[0].transaction_id


def get_public_work_changes_from(db: Session, public_work_version: int) -> list:
    versioned_class = version_class(PublicWorkDB)
    changes_list = db.query(versioned_class).filter(versioned_class.transaction_id > public_work_version).order_by(
        desc(versioned_class.transaction_id))
    changes_dict = {}

    for change in changes_list:
        if change.id not in changes_dict:
            if change.operation_type == Operation.DELETE:
                changes_dict[change.id] = PublicWorkDiff(
                    id=change.id,
                    operation=change.operation_type
                )
            else:
                try:
                    changes_dict[change.id] = PublicWorkDiff(
                        id=change.id,
                        name=change.name,
                        type_work_flag=change.type_work_flag,
                        address=change.address,
                        operation=change.operation_type
                    )
                except Exception:
                    print("Exception when parsing the public work")

    return list(changes_dict.values())
