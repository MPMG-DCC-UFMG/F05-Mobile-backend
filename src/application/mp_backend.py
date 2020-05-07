from fastapi import FastAPI
from .core import config
from .typework.routes import typeWorkRouter

mpApi = FastAPI()

mpApi.include_router(
    typeWorkRouter,
    prefix="/typeworks",
    tags=["typeworks"],
    responses={404: {"description": "Not found"}}
)
