from typing import List

from sqlalchemy.orm import Session

from src.application.collect.database.collectDB import CollectDB
from src.application.collect.models.collect import Collect


def get_all_collect(db: Session) -> List[Collect]:
    return db.query(CollectDB).all()


def add_collect(db: Session, collect: Collect) -> Collect:
    db_collect = collect.to_db()
    db.add(db_collect)
    db.commit()
    db.refresh(db_collect)
    return db_collect


def update_collect(db: Session, collect: Collect) -> Collect:
    db_collect = db.query(CollectDB).filter(CollectDB.id == collect.id).first()
    if db_collect:
        db_collect = collect.to_db()
        db.commit()
        db.refresh(db_collect)
        return db_collect
    else:
        return add_collect(db, collect)


def delete_collect(db: Session, collect_id: str) -> Collect:
    db_collect = db.query(CollectDB).filter(CollectDB.id == collect_id).first()
    if db_collect:
        db.delete(db_collect)
        db.commit()
    return db_collect
