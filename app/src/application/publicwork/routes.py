from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from application.address.database import repository as address_repository
from application.collect.database import repository as collect_repository
from application.photo.database import repository as photo_repository
from application.security.database import repository as security_repository
from application.core.database import get_db
from application.core.models.pagination import Pagination
from application.publicwork.database import \
    repository as public_work_repository
from application.publicwork.models.publicwork import PublicWork, PublicWorkDiff
from application.security.core.checker import admin_role
from application.shared.base_router import BaseRouter
from application.publicwork.models.publicworkPdf import PublicWorkPdfDTO
from application.publicwork.util.docxServiceById import generate_docx_by_id

class PublicWorkRouter(BaseRouter):
    public_work_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.public_work_router

    @staticmethod
    @public_work_router.get("/")
    async def get_all_public_work(db: Session = Depends(get_db)) -> List[PublicWork]:
        public_work_list = public_work_repository.get_public_work(db)
        return public_work_list

    @staticmethod
    @public_work_router.get("/queue")
    async def get_public_work_queue(db: Session = Depends(get_db)) -> List[PublicWork]:
      queue = public_work_repository.get_public_work_queue(db)
      return queue

    @staticmethod
    @public_work_router.get("/paginated")
    async def get_public_work_paginated(page: int = 1, per_page: int = 10,
                                        db: Session = Depends(get_db)) -> Pagination:
        public_work_list = public_work_repository.get_public_work_paginated(db, page, per_page)
        if public_work_list:
            return public_work_list
        else:
            raise HTTPException(status_code=402, detail="Invalid combination of pages")

    @staticmethod
    @public_work_router.post("/add", )
    async def add_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
        address_db = address_repository.add_address(db, public_work.address)
        public_work.address.id = address_db.id
        public_work_db = public_work_repository.add_public_work(db, public_work)
        public_work_db.address = address_db
        return public_work_db

    @staticmethod
    @public_work_router.put("/update", responses={403: {"description": "Operation forbidden"}})
    async def update_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
        address_db = address_repository.update_address(db, public_work.address)
        public_work.address.id = address_db.id
        public_work_db = public_work_repository.update_public_work(db, public_work)
        public_work_db.address = address_db
        if public_work_db and address_db:
            return public_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find public work to update")

    @staticmethod
    @public_work_router.post("/upsert", responses={403: {"description": "Operation forbidden"}})
    async def upsert_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
        address_db = address_repository.upsert_address(db, public_work.address)
        public_work.address.id = address_db.id
        public_work_db = public_work_repository.upsert_public_work(db, public_work)
        public_work_db.address = address_db
        if public_work_db and address_db:
            return public_work_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find public work to update")

    @staticmethod
    @public_work_router.delete("/delete", dependencies=[Depends(admin_role)],
                             responses={403: {"description": "Operation forbidden"}})
    async def delete_public_work(public_work_id: str, db: Session = Depends(get_db)) -> PublicWork:
        public_work_db = public_work_repository.delete_public_work(db, public_work_id)
        if public_work_db:
            public_work_db.address = None
            public_work_db.collect = []
            return public_work_db
        else:
            raise HTTPException(status_code=403, detail="Not able to find public work to delete")

    @staticmethod
    @public_work_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": public_work_repository.get_table_version(db)}

    @staticmethod
    @public_work_router.get("/changes")
    async def get_changes_from_version(version: int, db: Session = Depends(get_db)) -> List[PublicWorkDiff]:
        return public_work_repository.get_public_work_changes_from(db, version)

    @staticmethod
    @public_work_router.get("/count")
    async def get_public_work_count(db: Session = Depends(get_db)) -> int:
        return public_work_repository.count_public_work(db)
    
    @staticmethod
    @public_work_router.get("/{id}")
    async def get_public_work_by_id(id: str, db: Session = Depends(get_db)) -> PublicWork:
        return public_work_repository.get_public_work_by_id(db, id)

    @staticmethod
    @public_work_router.get("/citizen/queue")
    async def get_public_work_with_collect_in_queue(db: Session = Depends(get_db)) -> List[PublicWork]:
      return public_work_repository.get_public_works_with_collect_in_queue(db)

    @staticmethod
    @public_work_router.get("/reportDocx/{public_work_id}")
    async def generate_report_by_flag(public_work_id: str, db: Session = Depends(get_db)):
        public_work_db = public_work_repository.get_public_work_by_id(db, public_work_id)
        collects_db = collect_repository.get_public_work_collects(db, public_work_id)
        photos_db = []
        users_db = []
        for i in range(0, len(collects_db)):
            photos_db.append(photo_repository.get_photos_by_collect_id(db, collects_db[i].id))
            users_db.append(security_repository.get_user_by_email(db, collects_db[i].user_email))
        
        pdfDto = {
            "name": str(public_work_db.name),
            "address": public_work_db.address.street + ", " + public_work_db.address.number + " - " + public_work_db.address.city + "/"  + public_work_db.address.state,
            "content": [
                {"date": datetime.fromtimestamp(collects_db[i].date / 1000).strftime("%d/%m/%Y às %H:%M:%S"),
                "observations": str(collects_db[i].comments),
                "photos": [
                    {
                    "image_path": "../" + photo.filepath,
                    "description": photo.comment,
                    "latitude": str(photo.latitude),
                    "longitude": str(photo.longitude)
                    } for photo in photos_db[i]
                ],
                "inspector": {
                    "name": users_db[i].full_name,
                    "email": users_db[i].email,
                    "role": "Vistoriador do MPMG"
                }} for i in range(len(collects_db))
            ]
        }
        docx = generate_docx_by_id(PublicWorkPdfDTO.parse_obj(pdfDto))
        headers = {'Content-Disposition': f'attachment; filename={docx}'}
        return FileResponse(docx, headers=headers, media_type="application/docx")
