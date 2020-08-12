from typing import List, Dict

from application.shared.base_router import BaseRouter
from application.workstatus.database import repository
from application.workstatus.models.workStatus import WorkStatus
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from application.core.database import get_db


class WorkStatusRouter(BaseRouter):
    work_status_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.work_status_router

    @staticmethod
    @work_status_router.get("/")
    async def get_all_work_status(db: Session = Depends(get_db)) -> list:
        response = repository.get_work_status(db)
        return response

    @staticmethod
    @work_status_router.post("/add")
    async def add_work_status(work_status: WorkStatus, db: Session = Depends(get_db)) -> WorkStatus:
        response = repository.add_work_status(db, work_status)
        return response

    @staticmethod
    @work_status_router.put("/update", responses={403: {"description": "Operation forbidden"}})
    async def update_work_status(work_status: WorkStatus, db: Session = Depends(get_db)) -> WorkStatus:
        work_status_db = repository.update_work_status(db, work_status)
        if work_status_db:
            return work_status_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of work to update")

    @staticmethod
    @work_status_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
    async def delete_work_status(work_status_id: int, db: Session = Depends(get_db)) -> WorkStatus:
        work_status_db = repository.delete_work_status(db, work_status_id)
        if work_status_db:
            return work_status_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of work to delete")

    @staticmethod
    @work_status_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}
