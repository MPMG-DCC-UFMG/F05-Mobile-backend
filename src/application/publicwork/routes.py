from fastapi import APIRouter, Depends, HTTPException
from src.application.core.database import get_db
from sqlalchemy.orm import Session

from src.application.publicwork.models.publicwork import PublicWork
from src.application.publicwork.database import repository

public_work_router = APIRouter()


@public_work_router.get("/")
async def get_all_public_work(db: Session = Depends(get_db)) -> list:
    return repository.get_public_work(db)


@public_work_router.post("/add", )
async def add_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
    return repository.add_public_work(db, public_work)


@public_work_router.put("/update", responses={403: {"description": "Operation forbidden"}})
async def update_type_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
    pubic_work_db = repository.update_public_work(db, public_work)
    if pubic_work_db:
        return pubic_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find public work to update")


@public_work_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
async def delete_type_work(public_work_id: str, db: Session = Depends(get_db)) -> PublicWork:
    pubic_work_db = repository.delete_public_work(db, public_work_id)
    if pubic_work_db:
        return pubic_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find public work to delete")
