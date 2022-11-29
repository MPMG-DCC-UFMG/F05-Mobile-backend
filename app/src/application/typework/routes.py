from typing import Dict, List

from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from application.shared.response import Response
from application.typephoto.models.typePhoto import TypePhoto
from fastapi import APIRouter, Depends, HTTPException, FastAPI, Body
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
    @type_work_router.post("/add", dependencies=[Depends(admin_role)])
    async def add_type_work(type_work: TypeWork, db: Session = Depends(get_db)) -> TypeWork:
        return repository.add_type_work(db, type_work)

    @staticmethod
    @type_work_router.put("/update", dependencies=[Depends(admin_role)],
                          responses={403: {"description": "Operation forbidden"}})
    async def update_type_work(type_work: TypeWork, db: Session = Depends(get_db)) -> TypeWork:
        type_work_db = repository.update_type_work(db, type_work)
        if type_work_db:
            return type_work_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find type of work to update")

    @staticmethod
    @type_work_router.delete("/delete", dependencies=[Depends(admin_role)],
                           responses={403: {"description": "Operation forbidden"}})
    async def delete_type_work(type_work_id: int, db: Session = Depends(get_db)) -> TypeWork:
        type_work_db = repository.delete_type_work(db, type_work_id)
        if type_work_db:
            type_work_db.status_list = []
            return type_work_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find type of work to delete")

    @staticmethod
    @type_work_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}

    @staticmethod
    @type_work_router.post("/typePhoto/add", dependencies=[Depends(admin_role)])
    async def add_type_photo_to_type_work(type_work_id: int, type_photo_id: int,
                                          db: Session = Depends(get_db)) -> Response:
        result = repository.add_type_photo_to_type_work(db, type_work_id, type_photo_id)
        if result:
            return Response(success=result)
        else:
            raise HTTPException(status_code=603, detail="Not able to create association")

    @staticmethod
    @type_work_router.post("/typePhoto/update", dependencies=[Depends(admin_role)])
    async def update_type_photos_to_type_work(type_work_id: int = Body(...), type_photos: List[int] = Body(...),
                                              db: Session = Depends(get_db)) -> Response:
        result = repository.update_type_photos_to_type_work(db, type_work_id, type_photos)
        if result:
            return Response(success=result)
        else:
            raise HTTPException(status_code=603, detail="Not able to create association between type photos")

    @staticmethod
    @type_work_router.get("/typePhoto/all")
    async def get_type_photo_from_type_work(type_work_id: int, db: Session = Depends(get_db)) -> List[TypePhoto]:
        return repository.get_type_work_type_photos(db, type_work_id)

    @staticmethod
    @type_work_router.post("/workStatus/update", dependencies=[Depends(admin_role)])
    async def update_work_statuses_to_type_work(type_work_id: int = Body(...), work_statuses: List[int] = Body(...),
                                                db: Session = Depends(get_db)) -> Response:
        result = repository.update_work_statuses_of_type_work(db, type_work_id, work_statuses)
        if result:
            return Response(success=result)
        else:
            raise HTTPException(status_code=603, detail="Not able to create association between work status")

    @staticmethod
    @type_work_router.get("/workStatus/all")
    async def get_work_status_from_type_work(type_work_id: int, db: Session = Depends(get_db)) -> List[TypePhoto]:
        return repository.get_type_work_work_status(db, type_work_id)
