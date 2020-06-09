from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.application.typephoto.models.typePhoto import TypePhoto
from src.application.core.database import get_db
from src.application.typephoto.database import repository

type_photo_router = APIRouter()


@type_photo_router.get("/")
async def get_all_type_work(db: Session = Depends(get_db)) -> list:
    return repository.get_type_photo(db)


@type_photo_router.post("/add", )
async def add_type_work(type_photo: TypePhoto, db: Session = Depends(get_db)) -> TypePhoto:
    return repository.add_type_photo(db, type_photo)


@type_photo_router.put("/update", responses={403: {"description": "Operation forbidden"}})
async def update_type_work(type_photo: TypePhoto, db: Session = Depends(get_db)) -> TypePhoto:
    type_work_db = repository.update_type_photo(db, type_photo)
    if type_work_db:
        return type_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find type of work to update")


@type_photo_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
async def delete_type_work(type_photo_id: int, db: Session = Depends(get_db)) -> TypePhoto:
    type_work_db = repository.delete_type_photo(db, type_photo_id)
    if type_work_db:
        return type_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find type of photo to delete")


@type_photo_router.get("/version")
async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
    return {"version": repository.get_table_version(db)}
