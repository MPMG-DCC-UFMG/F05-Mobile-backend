from fastapi import FastAPI
import sqlalchemy as sa

from src.application.core import config
from src.application.core.database import Base, engine

from src.application.typework.routes import type_work_router
from src.application.publicwork.routes import public_work_router

sa.orm.configure_mappers()
Base.metadata.create_all(bind=engine)

mpApi = FastAPI()

mpApi.include_router(
    type_work_router,
    prefix="/typeworks",
    tags=["typeworks"],
    responses={404: {"description": "Not found"}}
)

mpApi.include_router(
    public_work_router,
    prefix="/publicworks",
    tags=["publicworks"],
    responses={404: {"description": "Not found"}}
)
