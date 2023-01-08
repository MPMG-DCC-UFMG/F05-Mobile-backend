from typing import List

from application.calendar.calendar_utils import get_today
from application.call.database.callDB import CallDB
from application.call.models.call import Call
from sqlalchemy import desc
from sqlalchemy.orm import Session


def get_all_calls(db: Session) -> List[Call]:
    return db.query(CallDB).order_by(desc("created_at")).all()


def get_call_by_id(db: Session, call_id: str) -> Call:
    return db.query(CallDB).get(call_id)


def get_admin_calls(db: Session, admin_email: str) -> List[Call]:
    return (
        db.query(CallDB)
        .filter(CallDB.admin_email == admin_email, CallDB.closed.is_(False))
        .order_by(desc("created_at"))
        .all()
    )


def get_admin_calls_history(db: Session, admin_email: str) -> List[Call]:
    return (
        db.query(CallDB)
        .filter(CallDB.admin_email == admin_email)
        .order_by(desc("created_at"))
        .all()
    )


def get_user_calls(db: Session, user_email: str) -> List[Call]:
    return (
        db.query(CallDB)
        .filter(CallDB.user_email == user_email, CallDB.closed.is_(False))
        .order_by(desc("created_at"))
        .all()
    )


def get_user_calls_history(db: Session, user_email: str) -> List[Call]:
    return (
        db.query(CallDB)
        .filter(CallDB.user_email == user_email)
        .order_by(desc("created_at"))
        .all()
    )


def open_call(db: Session, call: Call) -> Call:
    db_call = CallDB.from_model(call)
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def delete_call(db: Session, call_id: str) -> Call:
    db_call = db.query(CallDB).get(call_id)
    if db_call:
        db.delete(db_call)
        db.commit()
    return db_call


def close_call(db: Session, call_id: str) -> Call:
    db_call = db.query(CallDB).get(call_id)
    if db_call:
        db_call.closed = True
        db_call.closed_at = get_today()
        db.commit()
        db.refresh(db_call)
        return db_call
