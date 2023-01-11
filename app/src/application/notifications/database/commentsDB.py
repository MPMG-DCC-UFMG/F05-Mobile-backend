from sqlalchemy import Column, String, BigInteger

from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.notifications.models.comments import Comments

class CommentsDB(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    notification_id = Column(String)
    content = Column(String)
    user_email = Column(String)
    timestamp = Column(BigInteger)
    

    @classmethod
    def from_model(cls, comments: Comments):
        comments_db = CommentsDB(
            notification_id = comments.notification_id,
            content=comments.content,
            user_email=comments.user_email,
            timestamp=comments.timestamp
        )

        if comments.id and is_valid_uuid(comments.id):
            comments_db.id = comments.id

        return comments_db
