from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum.utils import version_class

from src.application.associations.database.association_tp_tw import AssociationTypePhPWDB
from src.application.associations.models.association import AssociationTypePhPW


def get_association_by_type_work_flag(db: Session, type_work_flag: int) -> List[AssociationTypePhPW]:
    return db.query(AssociationTypePhPWDB).filter(AssociationTypePhPWDB.type_work_flag == type_work_flag).all()


def get_all_associations(db: Session) -> List[AssociationTypePhPW]:
    return db.query(AssociationTypePhPWDB).all()


def get_table_version(db: Session) -> int:
    version = version_class(AssociationTypePhPWDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1


def add_association(db: Session, association: AssociationTypePhPW) -> AssociationTypePhPW:
    db_association = AssociationTypePhPWDB(type_work_flag=association.type_work_flag,
                                           type_photo_flag=association.type_photo_flag)
    db.add(db_association)
    db.commit()
    db.refresh(db_association)
    return db_association


def delete_association(db: Session, type_photo_flag: int, type_work_flag) -> AssociationTypePhPW:
    db_association = db.query(AssociationTypePhPWDB).filter(
        AssociationTypePhPWDB.type_work_flag == type_work_flag and
        AssociationTypePhPWDB.type_photo_flag == type_photo_flag).first()
    if (db_association):
        db.delete(db_association)
        db.commit()
    return db_association
