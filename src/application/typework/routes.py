from fastapi import APIRouter
from .models.typeWork import TypeWork

typeWorkRouter = APIRouter()

listTypeWorks = [TypeWork(name="Escola", flag=1), TypeWork(name="Creche", flag=2)]


@typeWorkRouter.get("/")
def get_all_type_work() -> list:
    return listTypeWorks


@typeWorkRouter.post("/add")
def add_type_work(type_work: TypeWork) -> TypeWork:
    listTypeWorks.append(type_work)
    return type_work


@typeWorkRouter.post("/version")
def get_table_version() -> int:
    return 1
