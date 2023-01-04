from application.calendar.calendar_utils import get_today
from application.call.models.call import Call
from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String


class CallDB(Base):
    __table_name__ = "call"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    created_at = Column(BigInteger, default=get_today())
    title = Column(String)
    finished = Column(Boolean, default=False)

    admin_email = Column(String, ForeignKey("user.email"))
    user_email = Column(String, ForeignKey("user.email"))

    @classmethod
    def from_model(cls, call: Call):
        call_db = CallDB(
            id=call.id,
            created_at=call.created_at,
            title=call.title,
            admin_email=call.admin_email,
            user_email=call.user_email,
            finished=call.finished,
        )

        if call.id and is_valid_uuid(call.id):
            call_db = call.id

        return call_db
