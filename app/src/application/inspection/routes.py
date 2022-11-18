from datetime import datetime
from typing import Dict, List

from application.collect.database import repository as collect_repository
from application.core.database import get_db
from application.inspection.database import repository
from application.inspection.models.inspection import Inspection, InspectionDiff
from application.inspection.models.inspectionPdf import InspectionPdfDTO
from application.inspection.util.pdfService import generate_pdf
from application.inspection.util.pdfServiceByFlag import generate_pdf_by_flag
from application.photo.database import repository as photo_repository
from application.publicwork.database import \
    repository as public_work_repository
from application.security.core.checker import admin_role
from application.security.database import repository as security_repository
from application.shared.base_router import BaseRouter
from application.shared.response import Response
from application.typephoto.models.typePhoto import TypePhoto
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


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
            raise HTTPException(status_code=603, detail="Not able to find inspections by public work id")

    @staticmethod
    @inspection_router.get(
        "/user/{user_email}",
    )
    async def get_inspection_by_user_email(user_email: str, db: Session = Depends(get_db)) -> list:
        inspection_db = repository.get_inspection_by_user_email(db, user_email)
        if inspection_db:
            return inspection_db
        else:
            raise HTTPException(status_code=603, detail="Not able to find inspection by user email")

    @staticmethod
    @inspection_router.get("/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_table_version(db)}

    @staticmethod
    @inspection_router.get("/changes")
    async def get_changes_from_version(version: int, db: Session = Depends(get_db)) -> List[InspectionDiff]:
        return repository.get_inspection_changes_from(db, version)

    @staticmethod
    @inspection_router.get("/count")
    async def get_inspection_count(db: Session = Depends(get_db)) -> int:
        return repository.count_inspection(db)

    @staticmethod
    @inspection_router.post("/report")
    async def generate_report(pdfDto: InspectionPdfDTO):
        pdf = generate_pdf(pdfDto)
        headers = {'Content-Disposition': f'attachment; filename={pdf}'}
        return FileResponse(pdf, headers=headers, media_type="application/pdf")

    @staticmethod
    @inspection_router.get("/report/{inspection_flag}")
    async def generate_report_by_flag(inspection_flag: int, db: Session = Depends(get_db)):
        inspection_db = repository.get_inspection_by_flag(db, inspection_flag)
        public_work_db = public_work_repository.get_public_work_by_id(db, inspection_db.public_work_id)
        collects_db = collect_repository.get_inspection_collects(db, inspection_flag)
        photos_db = photo_repository.get_photos_by_collect_id(db, collects_db[0].id)
        user_db = security_repository.get_user_by_email(db, collects_db[0].user_email)
        pdfDto = {
            "inspection_id": str(inspection_db.flag),
            "local": public_work_db.address.street + ", " + public_work_db.address.number + " - " + public_work_db.address.city + "/"  + public_work_db.address.state,
            "inspection_date": datetime.fromtimestamp(collects_db[0].date).strftime("%d/%m/%Y às %H:%M:%S"),
            "content": [
                {
                "image_path": "../" + photo.filepath,
                "description": photo.comment,
                "latitude": str(photo.latitude),
                "longitude": str(photo.longitude)
                } for photo in photos_db
            ],
            "inspector": {
                "name": user_db.full_name,
                "role": "Vistoriador do MPMG"
            }
        }
        print(pdfDto)
        pdf = generate_pdf_by_flag(InspectionPdfDTO.parse_obj(pdfDto))
        headers = {'Content-Disposition': f'attachment; filename={pdf}'}
        return FileResponse(pdf, headers=headers, media_type="application/pdf")
