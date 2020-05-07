from fastapi import FastAPI
from src.application.core import config
from src.application.typework.routes import type_work_router

from src.application.core.database import Base, engine

Base.metadata.create_all(bind=engine)

mpApi = FastAPI()

mpApi.include_router(
    type_work_router,
    prefix="/typeworks",
    tags=["typeworks"],
    responses={404: {"description": "Not found"}}
)
