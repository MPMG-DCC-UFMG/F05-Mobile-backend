from typing import List

from application.notifications.database.commentsDB import CommentsDB
from application.notifications.database.notificationDB import NotificationDB
from application.notifications.models.comments import Comments
from application.notifications.models.notification import Notification
from sqlalchemy import desc
from sqlalchemy.orm import Session


def get_all_notifications(db: Session) -> List[Notification]:
    return db.query(NotificationDB).order_by(desc("timestamp")).all()


def get_notification_by_id(db: Session, collect_id: str) -> List[Notification]:
    return db.query(NotificationDB).filter(NotificationDB.inspection_id == collect_id).all()


def add_notification(db: Session, notification: Notification) -> Notification:
    db_notification = NotificationDB.from_model(notification)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_all_comments(db: Session) -> List[Comments]:
    return db.query(CommentsDB).all()

def add_comments(db: Session, comments: Comments) -> Comments:
    db_comments = CommentsDB.from_model(comments)
    db.add(db_comments)
    db.commit()
    return db_comments

def get_comments_by_id(db: Session, notification_id: str) -> List[Comments]:
    return db.query(CommentsDB).filter(CommentsDB.notification_id == notification_id).all()
    
def delete_notification(db: Session, notification_id: str) -> Notification:
    db_notification = db.query(NotificationDB).filter(NotificationDB.id == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification
