from sqlalchemy import Column, String, BigInteger

from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.notifications.models.notification import Notification

class NotificationDB(Base):
    __tablename__ = "notification"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    title = Column(String)
    inspection_id = Column(String)
    content = Column(String)
    user_email = Column(String)
    timestamp = Column(BigInteger)

    @classmethod
    def from_model(cls, notification: Notification):
        notification_db = NotificationDB(
            title=notification.title,
            inspection_id=notification.inspection_id,
            content=notification.content,
            user_email=notification.user_email,
            timestamp=notification.timestamp
        )

        if notification.id and is_valid_uuid(notification.id):
            notification_db.id = notification.id

        return notification_db
