from typing import List

from application.typephoto.database.typePhotoDB import TypePhotoDB
from application.workstatus.database.workStatusDB import WorkStatusDB
from sqlalchemy import desc
from sqlalchemy.orm import Session

from application.inspection.models.inspection import Inspection
from application.inspection.database.inspectionDB import InspectionDB

from sqlalchemy_continuum.utils import version_class


def get_inspection(db: Session) -> list:
    db_inspection = db.query(InspectionDB).all()
    return list(map(lambda inspect: inspect.parse_to_inspect(), db_inspection))

def get_inspection_by_work_id(db: Session, public_work_id: int) -> list:
    db_inspection = db.query(InspectionDB).filter(InspectionDB.public_work_id == public_work_id)
    return list(map(lambda inspect: inspect.parse_to_inspect(), db_inspection))

def add_inspection(db: Session, inspect: Inspection) -> Inspection:
    db_inspect = InspectionDB.from_model(inspect)
    db.add(db_inspect)
    db.commit()
    db.refresh(db_inspect)
    return db_inspect.parse_to_inspect()

def update_inspection(db: Session, inspection: Inspection) -> Inspection:
    db_inspection = db.query(InspectionDB).filter(InspectionDB.flag == inspection.flag).first()
    if db_inspection:
        db_inspection.update(inspection)
        db.commit()
        db.refresh(db_inspection)
        return db_inspection


