from typing import List

from fastapi import APIRouter, Depends, HTTPException
from src.application.core.database import get_db
from sqlalchemy.orm import Session

from src.application.photo.models.photo import Photo
from src.application.photo.database import repository

photo_router = APIRouter()


@photo_router.get("/")
async def get_all_photos(db: Session = Depends(get_db)) -> List[Photo]:
    photo_list = repository.get_all_photos(db)
    return photo_list


@photo_router.post("/add")
async def add_photo(photo: Photo, db: Session = Depends(get_db)) -> Photo:
    return repository.add_photo(db, photo)
