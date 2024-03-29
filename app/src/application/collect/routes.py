from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from application.collect.database import repository
from application.collect.models.collect import Collect
from application.collect.models.collect_report import CollectReport
from application.core.database import get_db
from application.core.models.pagination import Pagination
from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter


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
    @collect_router.get("/citizen")
    async def get_all_citizen_collects(db: Session = Depends(get_db)) -> List[Collect]:
      return repository.get_all_citizen_collects(db)
    
    @staticmethod
    @collect_router.get("/citizen/queue")
    async def get_citizen_collect_queue(db: Session = Depends(get_db)) -> List[Collect]:
      return repository.get_citizen_collects_queue(db)

    @staticmethod
    @collect_router.get("/paginated")
    async def get_collect_paginated(page: int = 1, per_page: int = 20,
                                    db: Session = Depends(get_db)) -> Pagination:
        paginatedCollects = repository.get_all_collect_paginated(db, page, per_page)
        paginatedCollects.data = list(map(lambda collect: collect.parse_to_collect(), paginatedCollects.data))
        return paginatedCollects

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
    @collect_router.delete("/delete", dependencies=[Depends(admin_role)],
                         responses={403: {"description": "Operation forbidden"}})
    async def delete_collect(collect_id: str, db: Session = Depends(get_db)) -> Collect:
        collect_db = repository.delete_collect(db, collect_id)
        if collect_db:
            return collect_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find collect to delete")

    @staticmethod
    @collect_router.get("/publicWork")
    async def get_collect_by_public_work_id(public_work_id: str, db: Session = Depends(get_db)) -> List[Collect]:
        return repository.get_public_work_collects(db, public_work_id)

    @staticmethod
    @collect_router.get("/publicwork/citizen")
    async def get_citizen_collects_by_public_work_id(public_work_id: str, db: Session = Depends(get_db)) -> List[Collect]:
      return repository.get_public_work_citizen_collects(db, public_work_id)

    @staticmethod
    @collect_router.get("/month/count")
    async def get_collect_month_count(db: Session = Depends(get_db)) -> int:
        return repository.get_month_collects_count(db)

    @staticmethod
    @collect_router.get("/report/json")
    async def get_collect_report_json(public_work_id: str, db: Session = Depends(get_db)) -> List[CollectReport]:
        collects = repository.create_public_work_collect_report_json(db, public_work_id)
        return collects

    @staticmethod
    @collect_router.get("/report/json/file")
    async def get_collect_report_json_file(public_work_id: str, db: Session = Depends(get_db)) -> FileResponse:
        path = repository.create_public_work_collect_report_json_file(db, public_work_id)
        response = FileResponse(path, media_type='application/octet-stream', filename=public_work_id + ".json")
        response.headers["Content-Disposition"] = "attachment; filename={0}.json".format(public_work_id)
        return response
