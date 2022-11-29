from typing import Optional

from application.core.helpers import paginate
from application.core.models.pagination import Pagination
from application.publicwork.database.publicWorkDB import PublicWorkDB
from application.publicwork.models.publicwork import PublicWork, PublicWorkDiff
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import Operation, version_class


def get_public_work(db: Session) -> list:
    return db.query(PublicWorkDB).all()


def get_public_work_paginated(db: Session, page: int, per_page: int = 20) -> Optional[Pagination]:
    return paginate(db.query(PublicWorkDB), page, per_page)


def count_public_work(db: Session) -> int:
    return db.query(PublicWorkDB).count()


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


def get_public_work_by_id(db: Session, public_work_id: str) -> PublicWork:
    return db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work_id).first()


def update_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = db.query(PublicWorkDB).filter(PublicWorkDB.id == public_work.id).first()
    if db_public_work:
        db_public_work.update(public_work)
        db.commit()
        db.refresh(db_public_work)
        return db_public_work


def update_public_work_user_status(db: Session, public_work_id: str, user_status: int):
    public_work = get_public_work_by_id(db, public_work_id)
    public_work.user_status = user_status
    update_public_work(db, public_work)


def upsert_public_work(db: Session, public_work: PublicWork) -> PublicWork:
    db_public_work = update_public_work(db, public_work)
    if db_public_work:
        return db_public_work
    else:
        return add_public_work(db, public_work)


def get_table_version(db: Session) -> int:
    version = version_class(PublicWorkDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1


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
                    public_work = PublicWorkDiff(
                        id=change.id,
                        name=change.name,
                        type_work_flag=change.type_work_flag,
                        address=change.address,
                        operation=change.operation_type
                    )
                    if change.user_status:
                        public_work.user_status = change.user_status
                    changes_dict[change.id] = public_work
                except Exception:
                    print("Exception when parsing the public work")

    return list(changes_dict.values())
