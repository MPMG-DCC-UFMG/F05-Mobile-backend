from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from src.application.core.database import get_db
from sqlalchemy.orm import Session

from src.application.publicwork.models.publicwork import PublicWork
from src.application.publicwork.database import repository as public_work_repository

from src.application.address.database import repository as address_repository

public_work_router = APIRouter()


@public_work_router.get("/")
async def get_all_public_work(db: Session = Depends(get_db)) -> List[PublicWork]:
    public_work_list = public_work_repository.get_public_work(db)
    return public_work_list


@public_work_router.post("/add", )
async def add_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
    address_db = address_repository.add_address(db, public_work.address)
    public_work.address.id = address_db.id
    public_work_db = public_work_repository.add_public_work(db, public_work)
    public_work_db.address = address_db
    return public_work_db


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


@public_work_router.post("/upsert", responses={403: {"description": "Operation forbidden"}})
async def upsert_public_work(public_work: PublicWork, db: Session = Depends(get_db)) -> PublicWork:
    address_db = address_repository.upsert_address(db, public_work.address)
    public_work.address.id = address_db.id
    public_work_db = public_work_repository.upsert_public_work(db, public_work)
    public_work_db.address = address_db
    if public_work_db and address_db:
        return public_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find public work to update")


@public_work_router.post("/delete", responses={403: {"description": "Operation forbidden"}})
async def delete_public_work(public_work_id: str, db: Session = Depends(get_db)) -> PublicWork:
    pubic_work_db = public_work_repository.delete_public_work(db, public_work_id)
    if pubic_work_db:
        return pubic_work_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find public work to delete")


@public_work_router.get("/version")
async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
    return {"version": public_work_repository.get_table_version(db)}
