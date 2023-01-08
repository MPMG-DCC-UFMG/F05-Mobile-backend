from typing import List

from application.call.database import repository
from application.call.models.call import Call
from application.core.database import get_db
from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session


class CallRouter(BaseRouter):
    call_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.call_router

    @classmethod
    @call_router.get("/", dependencies=[Depends(admin_role)])
    async def get_all_calls(db: Session = Depends(get_db)) -> List[Call]:
        return repository.get_all_calls(db)

    @classmethod
    @call_router.get("/{call_id}")
    async def get_call_by_id(call_id: str, db: Session = Depends(get_db)) -> Call:
        return repository.get_call_by_id(db, call_id)

    @classmethod
    @call_router.get("/admin/{admin_email}")
    async def get_admin_open_calls(
        admin_email: str, db: Session = Depends(get_db)
    ) -> List[Call]:
        return repository.get_admin_calls(db, admin_email)

    @classmethod
    @call_router.get("/admin/history/{admin_email}", dependencies=[Depends(admin_role)])
    async def get_admin_calls_history(
        admin_email: str, db: Session = Depends(get_db)
    ) -> List[Call]:
        return repository.get_admin_calls_history(db, admin_email)

    @classmethod
    @call_router.get("/user/{user_email}")
    async def get_user_open_calls(
        user_email: str, db: Session = Depends(get_db)
    ) -> List[Call]:
        return repository.get_user_calls(db, user_email)

    @classmethod
    @call_router.get("/user/history/{user_email}")
    async def get_user_calls_history(
        user_email: str, db: Session = Depends(get_db)
    ) -> List[Call]:
        return repository.get_user_calls_history(db, user_email)

    @classmethod
    @call_router.post("/", dependencies=[Depends(admin_role)])
    async def open_call(call: Call, db: Session = Depends(get_db)) -> Call:
        return repository.open_call(db, call)

    @classmethod
    @call_router.put("/{call_id}", dependencies=[Depends(admin_role)])
    async def close_call(call_id: str, db: Session = Depends(get_db)) -> Call:
        return repository.close_call(db, call_id)

    @classmethod
    @call_router.delete("/{call_id}", dependencies=[Depends(admin_role)])
    async def delete_call(call_id: str, db: Session = Depends(get_db)) -> Call:
        return repository.delete_call(db, call_id)
