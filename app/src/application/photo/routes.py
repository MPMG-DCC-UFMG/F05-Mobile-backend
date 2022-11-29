from typing import List

from application.core.database import get_db
from application.photo.database import repository
from application.photo.models.photo import Photo
from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


class PhotoRouter(BaseRouter):
    photo_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.photo_router

    @staticmethod
    @photo_router.get("/")
    async def get_all_photos(db: Session = Depends(get_db)) -> List[Photo]:
        photo_list = repository.get_all_photos(db)
        return photo_list

    @staticmethod
    @photo_router.post("/add")
    async def add_photo(photo: Photo, db: Session = Depends(get_db)) -> Photo:
        return repository.add_photo(db, photo)

    @staticmethod
    @photo_router.get("/collect/{collect_id}")
    async def get_photos_from_collect(collect_id: str, db: Session = Depends(get_db)) -> List[Photo]:
        return repository.get_photos_by_collect_id(db, collect_id)

    @staticmethod
    @photo_router.post("/delete", dependencies=[Depends(admin_role)],
                       responses={403: {"description": "Operation forbidden"}})
    async def delete_photo(photo_id: str, db: Session = Depends(get_db)) -> Photo:
        photo_db = repository.delete_photo(db, photo_id)
        if photo_db:
            return photo_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find photo to delete")
