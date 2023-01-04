from typing import List

from application.message.database.messageDB import MessageDB
from application.message.model.message import Message
from sqlalchemy import desc
from sqlalchemy.orm import Session


def get_messages_from_call(db: Session, call_id: str) -> List[Message]:
    return (
        db.query(MessageDB)
        .filter(MessageDB.call_id == call_id)
        .order_by(desc("timestamp"))
        .all()
    )


def send_message(db: Session, message: Message) -> Message:
    db_message = MessageDB.from_model(message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: str) -> Message:
    db_message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
    if db_message:
        db_message.update({MessageDB.text: "Mensagem apagada"})
        db.commit()
        db.refresh()
        return db_message
