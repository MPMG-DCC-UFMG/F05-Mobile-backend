from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import version_class

from application.workstatus.database.workStatusDB import WorkStatusDB
from application.workstatus.models.workStatus import WorkStatus


def get_work_status(db: Session) -> list:
    db_work_status = db.query(WorkStatusDB).all()
    return list(map(lambda work_status: work_status.parse_to_work_status(), db_work_status))

def get_work_status_by_id(work_status_id: int, db: Session) -> WorkStatus:
  db_work_status = db.query(WorkStatusDB).filter(WorkStatusDB.flag == work_status_id).first()
  return db_work_status


def add_work_status(db: Session, work_status: WorkStatus) -> WorkStatus:
    db_work_status = WorkStatusDB.from_model(work_status)
    db.add(db_work_status)
    db.commit()
    db.refresh(db_work_status)
    return db_work_status


def delete_work_status(db: Session, work_status_id: int) -> WorkStatus:
    db_work_status = db.query(WorkStatusDB).filter(WorkStatusDB.flag == work_status_id).first()
    if db_work_status:
        db.delete(db_work_status)
        db.commit()
    return db_work_status


def update_work_status(db: Session, work_status: WorkStatus) -> WorkStatus:
    db_work_status = db.query(WorkStatusDB).filter(WorkStatusDB.flag == work_status.flag).first()
    if db_work_status:
        db_work_status.update(work_status)
        db.commit()
        db.refresh(db_work_status)
        return db_work_status


def get_table_version(db: Session) -> int:
    version = version_class(WorkStatusDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1
