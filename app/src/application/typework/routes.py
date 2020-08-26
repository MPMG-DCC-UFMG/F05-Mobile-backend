from typing import Dict, List

from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from application.typework.models.typeWork import TypeWork
from application.core.database import get_db
from application.typework.database import repository


class TypeWorkRouter(BaseRouter):
    type_work_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.type_work_router

    @staticmethod
    @type_work_router.get("/")
    async def get_all_type_work(db: Session = Depends(get_db)) -> list:
        return repository.get_type_work(db)

    @staticmethod
    @type_work_router.post("/add", )
    async def add_type_work(type_work: TypeWork, db: Session = Depends(get_db)) -> TypeWork:
        return repository.add_type_work(db, type_work)

    @staticmethod
    @type_work_router.put("/update", responses={403: {"description": "Operation forbidden"}})
    async def update_type_work(type_work: TypeWork, db: Session = Depends(get_db)) -> TypeWork:
        type_work_db = repository.update_type_work(db, type_work)
        if type_work_db:
            return type_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of work to update")

    @staticmethod
    @type_work_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
    async def delete_type_work(type_work_id: int, db: Session = Depends(get_db)) -> TypeWork:
        type_work_db = repository.delete_type_work(db, type_work_id)
        if type_work_db:
            type_work_db.status_list = []
            return type_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of work to delete")

    @staticmethod
    @type_work_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}
