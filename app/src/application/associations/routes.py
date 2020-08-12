from typing import Dict, List

from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from application.core.database import get_db
from application.associations.database import repository
from application.associations.models.association import AssociationTypePhPW


class AssociationRouter(BaseRouter):
    association_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.association_router

    @staticmethod
    @association_router.get("/typework")
    async def get_all_typework_type_photos(type_work_flag: int, db: Session = Depends(get_db)) -> list:
        return repository.get_association_by_type_work_flag(db, type_work_flag)

    @staticmethod
    @association_router.post("/tptw/add")
    async def add_type_photo_to_type_work(association: AssociationTypePhPW,
                                          db: Session = Depends(get_db)) -> AssociationTypePhPW:
        return repository.add_association(db, association)

    @staticmethod
    @association_router.post("/tptw/delete")
    async def delete_association(type_work_flag: int, type_photo_flag: int,
                                 db: Session = Depends(get_db)) -> AssociationTypePhPW:
        association_db = repository.delete_association(db, type_photo_flag, type_work_flag)
        if association_db:
            return association_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find association to delete")

    @staticmethod
    @association_router.get("/tptw/all")
    async def get_all_associations(db: Session = Depends(get_db)) -> list:
        return repository.get_all_associations(db)

    @staticmethod
    @association_router.get("/tptw/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}
