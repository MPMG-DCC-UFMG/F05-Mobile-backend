from typing import Dict, List

from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from application.shared.response import Response
from application.typephoto.models.typePhoto import TypePhoto
from fastapi import APIRouter, Depends, HTTPException, FastAPI, Body
from sqlalchemy.orm import Session

from application.core.database import get_db
from application.inspection.database import repository
from application.inspection.models.inspection import Inspection, InspectionDiff
from application.inspection.database import repository as inspection_repository


class InspectionRouter(BaseRouter):
    inspection_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.inspection_router

    @staticmethod
    @inspection_router.get("/")
    async def get_all_inspections(db: Session = Depends(get_db)) -> list:
        return repository.get_inspection(db)

    @staticmethod
    @inspection_router.post(
        "/add",
    )
    async def add_inspection(inspection: Inspection, db: Session = Depends(get_db)) -> Inspection:
        response = repository.add_inspection(db, inspection)
        return response

    @staticmethod
    @inspection_router.put("/update", responses={403: {"description": "Operation forbidden"}})
    async def update_inspection(inspection: Inspection, db: Session = Depends(get_db)) -> Inspection:
        inspection_db = repository.update_inspection(db, inspection)
        if inspection_db:
            return inspection_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find type of work to update")

    @staticmethod
    @inspection_router.get(
        "/publicwork/{public_work_id}",
    )
    async def get_inspection_by_work_id(public_work_id: str, db: Session = Depends(get_db)) -> list:
        inspection_db = repository.get_inspection_by_work_id(db, public_work_id)
        if inspection_db:
            return inspection_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find type of work to update")

    @staticmethod
    @inspection_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": inspection_repository.get_table_version(db)}

    @staticmethod
    @inspection_router.get("/changes")
    async def get_changes_from_version(version: int, db: Session = Depends(get_db)) -> List[InspectionDiff]:
        return inspection_repository.get_inspection_changes_from(db, version)

    @staticmethod
    @inspection_router.get("/count")
    async def get_inspection_count(db: Session = Depends(get_db)) -> int:
        return inspection_repository.count_inspection(db)
