from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa

from application.core import config
from application.core.database import Base, engine

from application.typework.routes import type_work_router
from application.publicwork.routes import public_work_router
from application.collect.routes import collect_router
from application.photo.routes import photo_router
from application.image.routes import images_router
from application.typephoto.routes import type_photo_router
from application.address.routes import address_router
from application.associations.routes import association_router
from application.security.routes import security_router

sa.orm.configure_mappers()
Base.metadata.create_all(bind=engine)

mpApi = FastAPI(
    title='F05 Backend API',
    description='API backend for the project F05',
    version="1.1.0",
    openapi_prefix=config.settings.api_prefix
)

origins = ["*"]

mpApi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mpApi.include_router(
    type_work_router,
    prefix="/typeworks",
    tags=["typeworks"],
    responses={404: {"description": "Type Work not found"}}
)

mpApi.include_router(
    public_work_router,
    prefix="/publicworks",
    tags=["publicworks"],
    responses={404: {"description": "Public Work not found"}}
)

mpApi.include_router(
    collect_router,
    prefix="/collects",
    tags=["collects"],
    responses={404: {"description": "Collect not found"}}
)

mpApi.include_router(
    photo_router,
    prefix="/photos",
    tags=["photos"],
    responses={404: {"description": "Photo not found"}}
)

mpApi.include_router(
    images_router,
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Image not found"}}
)

mpApi.include_router(
    type_photo_router,
    prefix="/typephotos",
    tags=["typephotos"],
    responses={404: {"description": "Type Photo not found"}}
)

mpApi.include_router(
    address_router,
    prefix="/address",
    tags=["address"],
    responses={404: {"description": "Address not found"}}
)

mpApi.include_router(
    association_router,
    prefix="/association",
    tags=["association"],
    responses={404: {"description": "Association not found"}}
)

mpApi.include_router(
    security_router,
    prefix="/security",
    tags=["security"],
    responses={404: {"description": "Not authorized"}}
)
