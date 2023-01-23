from typing import List

from application.core.database import get_db
from application.notifications.database import repository
from application.notifications.models.comments import Comments
from application.notifications.models.notification import Notification
from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


class NotificationRouter(BaseRouter):
    notification_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.notification_router

    @staticmethod
    @notification_router.get("/")
    async def get_all_notifications(db: Session = Depends(get_db)) -> List[Notification]:
        notification_list = repository.get_all_notifications(db)
        return notification_list

    @staticmethod
    @notification_router.post("/add")
    async def add_notification(notification: Notification, db: Session = Depends(get_db)) -> Notification:
        return repository.add_notification(db, notification)

    @staticmethod
    @notification_router.get("/{notification_id}")
    async def get_notification_from(notification_id: str, db: Session = Depends(get_db)) -> List[Notification]:
        return repository.get_notifications_by_id(db, notification_id)

    @staticmethod
    @notification_router.delete("/delete", dependencies=[Depends(admin_role)],
                       responses={403: {"description": "Operation forbidden"}})
    async def delete_notification(notification_id: str, db: Session = Depends(get_db)) -> Notification:
        notification_db = repository.delete_notification(db, notification_id)
        if notification_db:
            return notification_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find photo to delete")


    @staticmethod
    @notification_router.get("/comments/all")
    async def get_all_comments(db: Session = Depends(get_db)) -> List[Comments]:
        comments_list = repository.get_all_comments(db)
        return comments_list

    @staticmethod
    @notification_router.post("/add/comments")
    async def add_comments(comments: Comments, db: Session = Depends(get_db)) -> Comments:
        return repository.add_comments(db, comments)

    @staticmethod
    @notification_router.get("/comments/{notification_id}")
    async def get_comments_from_notification(notification_id: str, db: Session = Depends(get_db)) -> List[Comments]:
        return repository.get_comments_by_id(db, notification_id)
