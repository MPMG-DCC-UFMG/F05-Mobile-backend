from application.security.core.api_key import API_KEY_NAME, get_api_key
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa

from application.core import config
from application.core.database import Base, engine

from application.typework.routes import TypeWorkRouter
from application.publicwork.routes import PublicWorkRouter
from application.collect.routes import CollectRouter
from application.photo.routes import PhotoRouter
from application.image.routes import ImageRouter
from application.typephoto.routes import TypePhotoRouter
from application.address.routes import AddressRouter
from application.associations.routes import AssociationRouter
from application.security.routes import SecurityRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.responses import JSONResponse

sa.orm.configure_mappers()
Base.metadata.create_all(bind=engine)

mpApi = FastAPI(
    title='F05 Backend API',
    description='API backend for the project F05',
    version="1.2.0",
    openapi_prefix=config.settings.api_prefix,
    docs_url=None,
    redoc_url=None,
)

origins = ["*"]

mpApi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mpApi.add_middleware(SentryAsgiMiddleware)

routes = [TypeWorkRouter("typeworks", mpApi, [Depends(get_api_key)]),
          PublicWorkRouter("publicworks", mpApi, [Depends(get_api_key)]),
          CollectRouter("collects", mpApi, [Depends(get_api_key)]),
          PhotoRouter("photos", mpApi, [Depends(get_api_key)]),
          ImageRouter("images", mpApi, [Depends(get_api_key)]),
          TypePhotoRouter("typephotos", mpApi, [Depends(get_api_key)]),
          AddressRouter("address", mpApi, [Depends(get_api_key)]),
          AssociationRouter("association", mpApi, [Depends(get_api_key)]),
          SecurityRouter("security", mpApi, [Depends(get_api_key)])]

for route in routes:
    route.apply_route()


@mpApi.get("/")
async def homepage():
    return "Welcome to the Trena API!"


@mpApi.get("/docs", tags=["docs"], dependencies=[Depends(get_api_key)])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(
        openapi_url="{0}{1}?{2}={3}".format(config.settings.api_prefix, mpApi.openapi_url, API_KEY_NAME, api_key),
        title="docs")
    return response
