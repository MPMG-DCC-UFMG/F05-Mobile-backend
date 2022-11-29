from typing import Dict, List

from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from application.typephoto.models.typePhoto import TypePhoto
from application.core.database import get_db
from application.typephoto.database import repository


class TypePhotoRouter(BaseRouter):
    type_photo_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.type_photo_router

    @staticmethod
    @type_photo_router.get("/")
    async def get_all_type_work(db: Session = Depends(get_db)) -> list:
        return repository.get_type_photo(db)

    @staticmethod
    @type_photo_router.post("/add", dependencies=[Depends(admin_role)])
    async def add_type_work(type_photo: TypePhoto, db: Session = Depends(get_db)) -> TypePhoto:
        return repository.add_type_photo(db, type_photo)

    @staticmethod
    @type_photo_router.put("/update", dependencies=[Depends(admin_role)],
                           responses={403: {"description": "Operation forbidden"}})
    async def update_type_work(type_photo: TypePhoto, db: Session = Depends(get_db)) -> TypePhoto:
        type_work_db = repository.update_type_photo(db, type_photo)
        if type_work_db:
            return type_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of work to update")

    @staticmethod
    @type_photo_router.delete("/delete", dependencies=[Depends(admin_role)],
                            responses={403: {"description": "Operation forbidden"}})
    async def delete_type_work(type_photo_id: int, db: Session = Depends(get_db)) -> TypePhoto:
        type_work_db = repository.delete_type_photo(db, type_photo_id)
        if type_work_db:
            return type_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find type of photo to delete")

    @staticmethod
    @type_photo_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}
