from application.calendar.calendar_utils import get_today
from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid
from application.message.model.message import Message
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String


class MessageDB(Base):
    __tablename__ = "message"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    timestamp = Column(BigInteger, default=get_today())
    text = Column(String)
    readed = Column(Boolean, default=False)

    sender_email = Column(String, ForeignKey("user.email"))
    receiver_email = Column(String, ForeignKey("user.email"))
    call_id = Column(String, ForeignKey("call.id"))

    @classmethod
    def from_model(cls, message: Message):
        message_db = MessageDB(
            id=message.id,
            timestamp=message.timestamp,
            text=message.text,
            sender_email=message.sender_email,
            receiver_email=message.receiver_email,
            readed=message.readed,
            call_id = message.call_id
        )

        if message.id and is_valid_uuid(message.id):
            message_db.id = message.id

        return message_db
