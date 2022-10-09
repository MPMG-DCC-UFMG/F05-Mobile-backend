from typing import List

from application.typephoto.database.typePhotoDB import TypePhotoDB
from application.workstatus.database.workStatusDB import WorkStatusDB
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import version_class, Operation

from application.inspection.models.inspection import Inspection, InspectionDiff
from application.inspection.database.inspectionDB import InspectionDB


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


def get_table_version(db: Session) -> int:
    version = version_class(InspectionDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1


def get_inspection_changes_from(db: Session, inspection_version: int) -> list:
    versioned_class = version_class(InspectionDB)
    changes_list = (
        db.query(versioned_class)
        .filter(versioned_class.transaction_id > inspection_version)
        .order_by(desc(versioned_class.transaction_id))
    )
    changes_dict = {}

    for change in changes_list:
        if change.id not in changes_dict:
            if change.operation_type == Operation.DELETE:
                changes_dict[change.id] = InspectionDiff(id=change.id, operation=change.operation_type)
            else:
                try:
                    inspection = InspectionDiff(
                        id=change.id,
                        name=change.name,
                        type_work_flag=change.type_work_flag,
                        address=change.address,
                        operation=change.operation_type,
                    )
                    if change.user_status:
                        inspection.user_status = change.user_status
                    changes_dict[change.id] = inspection
                except Exception:
                    print("Exception when parsing the inspection")

    return list(changes_dict.values())
