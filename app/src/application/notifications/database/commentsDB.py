from application.calendar.calendar_utils import get_today
from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid
from application.notifications.models.comments import Comments
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String


class CommentsDB(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    timestamp = Column(BigInteger, default=get_today())
    content = Column(String)

    receive_email = Column(String, ForeignKey("user.email"))
    send_email = Column(String, ForeignKey("user.email"))
    notification_id = Column(String, ForeignKey("notification.id"))
    

    @classmethod
    def from_model(cls, comments: Comments):
        comments_db = CommentsDB(
            notification_id = comments.notification_id,
            content=comments.content,
            receive_email=comments.receive_email,
            send_email=comments.send_email,
            timestamp = comments.timestamp
        )

        if comments.id and is_valid_uuid(comments.id):
            comments_db.id = comments.id

        return comments_db
