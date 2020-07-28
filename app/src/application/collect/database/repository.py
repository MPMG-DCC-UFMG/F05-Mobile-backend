from typing import List

from sqlalchemy.orm import Session

from application.collect.database.collectDB import CollectDB
from application.collect.models.collect import Collect


def get_all_collect(db: Session) -> List[Collect]:
    return db.query(CollectDB).all()


def add_collect(db: Session, collect: Collect) -> Collect:
    db_collect = CollectDB.from_model(collect)
    db.add(db_collect)
    db.commit()
    db.refresh(db_collect)
    return db_collect


def update_collect(db: Session, collect: Collect) -> Collect:
    db_collect = db.query(CollectDB).filter(CollectDB.id == collect.id).first()
    if db_collect:
        db_collect.update(collect)
        db.commit()
        db.refresh(db_collect)
        return db_collect
    else:
        return add_collect(db, collect)


def upsert_collect(db: Session, collect: Collect) -> Collect:
    db_collect = update_collect(db, collect)
    if db_collect:
        return db_collect
    else:
        return add_collect(db, collect)


def delete_collect(db: Session, collect_id: str) -> Collect:
    db_collect = db.query(CollectDB).filter(CollectDB.id == collect_id).first()
    if db_collect:
        db.delete(db_collect)
        db.commit()
        db_collect.photos = []
    return db_collect
