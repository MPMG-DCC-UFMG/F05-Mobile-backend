from typing import List

from application.core.database import get_db
from application.shared.base_router import BaseRouter
from application.ws02.utils.oauth import client, get_login_url, get_user_info
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


class Wso2Router(BaseRouter):
    wso2_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.wso2_router

    @wso2_router.get("/authws02")
    def ws02(request: Request):
        return get_login_url()

    @wso2_router.get("/logoutcallback")
    def logout():
        return RedirectResponse(client.end_session_endpoint)

    @wso2_router.get(
        "/logincallback",
    )
    def callback(request: Request, db: Session = Depends(get_db)):
        params = request.query_params
        return get_user_info(params, db)
