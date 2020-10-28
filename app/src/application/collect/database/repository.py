from pathlib import Path
from typing import List

from sqlalchemy.orm import Session

from application.collect.database.collectDB import CollectDB
from application.collect.models.collect import Collect
from application.collect.models.collect_report import CollectReport

from application.calendar.calendar_utils import get_first_day_of_month
from application.file.file_utils import create_json_file_from_list

import application.publicwork.database.repository as public_work_repository


def get_all_collect(db: Session) -> List[Collect]:
    return db.query(CollectDB).all()


def get_public_work_collects(db: Session, public_work_id: str) -> List[Collect]:
    return db.query(CollectDB).filter(CollectDB.public_work_id == public_work_id).all()


def add_collect(db: Session, collect: Collect) -> Collect:
    db_collect = CollectDB.from_model(collect)
    db.add(db_collect)
    public_work_repository.update_public_work_user_status(db, collect.public_work_id, collect.public_work_status)
    db.commit()
    db.refresh(db_collect)
    return db_collect


def update_collect(db: Session, collect: Collect) -> Collect:
    db_collect = db.query(CollectDB).filter(CollectDB.id == collect.id).first()
    if db_collect:
        db_collect.update(collect)
        public_work_repository.update_public_work_user_status(db, collect.public_work_id, collect.public_work_status)
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


def get_month_collects_count(db: Session) -> int:
    first_day = get_first_day_of_month()
    return db.query(CollectDB).filter(CollectDB.date > first_day).count()


def create_public_work_collect_report_csv(db: Session, public_work_id: str) -> str:
    collects = db.query(CollectDB).filter(CollectDB.public_work_id == public_work_id).all()
    parsed_collects = []
    for collect in collects:
        parsed_collects.append(CollectReport.from_orm(collect))
    return "created"


def create_public_work_collect_report_json(db: Session, public_work_id: str) -> List[CollectReport]:
    collects = db.query(CollectDB).filter(CollectDB.public_work_id == public_work_id).all()
    parsed_collects = []
    for collect in collects:
        parsed_collects.append(CollectReport.from_orm(collect))
    return parsed_collects


def create_public_work_collect_report_json_file(db: Session, public_work_id: str) -> Path:
    parsed_collects = create_public_work_collect_report_json(db, public_work_id)
    file_destination = create_json_file_from_list(filename=public_work_id, data=parsed_collects)
    return file_destination
