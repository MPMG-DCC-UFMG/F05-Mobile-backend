from typing import List

from application.core.base_router import BaseRouter
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from application.core.database import get_db
from sqlalchemy.orm import Session

from application.collect.models.collect import Collect

from application.collect.database import repository


class CollectRouter(BaseRouter):
    collect_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.collect_router

    @staticmethod
    @collect_router.get("/")
    async def get_all_collect(db: Session = Depends(get_db)) -> List[Collect]:
        return repository.get_all_collect(db)

    @staticmethod
    @collect_router.post("/add")
    async def add_collect(collect: Collect, db: Session = Depends(get_db)) -> Collect:
        collect_db = repository.add_collect(db, collect)
        return collect_db

    @staticmethod
    @collect_router.put("/update", responses={403: {"description": "Operation forbidden"}})
    async def update_collect(collect: Collect, db: Session = Depends(get_db)) -> Collect:
        collect_db = repository.update_collect(db, collect)
        if collect_db:
            return collect_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find collect to update")

    @staticmethod
    @collect_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
    async def delete_collect(collect_id: str, db: Session = Depends(get_db)) -> Collect:
        collect_db = repository.delete_collect(db, collect_id)
        if collect_db:
            return collect_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find collect to delete")
