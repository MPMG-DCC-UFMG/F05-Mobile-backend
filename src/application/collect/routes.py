from typing import List

from fastapi import APIRouter, Depends, HTTPException
from src.application.core.database import get_db
from sqlalchemy.orm import Session

from src.application.collect.models.collect import Collect
from src.application.collect.database.collectDB import CollectDB

from src.application.collect.database import repository

collect_router = APIRouter()


@collect_router.get("/")
async def get_all_collect(db: Session = Depends(get_db)) -> List[Collect]:
    return repository.get_all_collect(db)


@collect_router.post("/add")
async def add_collect(collect: Collect, db: Session = Depends(get_db)) -> Collect:
    collect_db = repository.add_collect(db, collect)
    return collect_db


@collect_router.put("/update", responses={403: {"description": "Operation forbidden"}})
async def update_collect(collect: Collect, db: Session = Depends(get_db)) -> Collect:
    collect_db = repository.update_collect(db, collect)
    if collect_db:
        return collect_db
    else:
        raise HTTPException(status_code=403, detail="Not able to find collect to update")
