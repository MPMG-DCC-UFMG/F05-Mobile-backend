from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.application.typework.models.typeWork import TypeWork
from src.application.core.database import get_db
from src.application.typework.database import repository

type_work_router = APIRouter()

listTypeWorks = [TypeWork(name="Escola", flag=1), TypeWork(name="Creche", flag=2)]


@type_work_router.get("/")
def get_all_type_work(db: Session = Depends(get_db)) -> list:
    return repository.get_type_work(db)


@type_work_router.post("/add", )
def add_type_work(type_work: TypeWork, db: Session = Depends(get_db)) -> TypeWork:
    return repository.add_type_work(db, type_work)


@type_work_router.post("/version")
def get_table_version(db: Session = Depends(get_db)) -> int:
    repository.get_table_version(db)
    return 1
