from application.calendar.calendar_utils import get_today
from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid
from application.notifications.models.notification import Notification
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String


class NotificationDB(Base):
    __tablename__ = "notification"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String)
    content = Column(String)
    chat_close = Column(Boolean)
    answer = Column(Boolean)
    timestamp = Column(BigInteger, default=get_today())

    user_email = Column(String, ForeignKey("user.email"))
    inspection_id = Column(String, ForeignKey("inspection.flag"))

    @classmethod
    def from_model(cls, notification: Notification):
        notification_db = NotificationDB(
            title=notification.title,
            inspection_id=notification.inspection_id,
            content=notification.content,
            user_email=notification.user_email,
            chat_close=notification.chat_close,
            answer=notification.answer,
            timestamp = notification.timestamp
        )

        if notification.id and is_valid_uuid(notification.id):
            notification_db.id = notification.id

        return notification_db
