import contextlib
import warnings
from typing import List

import requests
from application.core.config import settings
from application.core.database import get_db
from application.security.database import repository
from application.security.models.user import User
from application.shared.base_router import BaseRouter
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from oic import rndstr
from oic.oic import Client
from oic.oic.message import (
    AuthorizationResponse,
    ProviderConfigurationResponse,
    RegistrationResponse,
)
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from sqlalchemy.orm import Session
from urllib3.exceptions import InsecureRequestWarning

inner_state = rndstr()
nonce = rndstr()
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)


@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    old_merge_environment_settings = requests.Session.merge_environment_settings

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        opened_adapters.add(self.get_adapter(url))
        settings = old_merge_environment_settings(
            self, url, proxies, stream, verify, cert
        )
        settings["verify"] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


def get_login_url():
    WS02_ISSUER = settings.ws02_issuer
    info_issuer = {}

    with no_ssl_verification():
        info_issuer = requests.get(
            "{}/oauth2/oidcdiscovery/.well-known/openid-configuration".format(
                WS02_ISSUER
            )
        ).json()

        op_info = ProviderConfigurationResponse(
            version="1.0",
            issuer=info_issuer["issuer"],
            authorization_endpoint=info_issuer["authorization_endpoint"],
            token_endpoint=info_issuer["token_endpoint"],
            jwks_uri=info_issuer["jwks_uri"],
            userinfo_endpoint=info_issuer["userinfo_endpoint"],
            revocation_endpoint=info_issuer["revocation_endpoint"],
            introspection_endpoint=info_issuer["introspection_endpoint"],
            end_session_endpoint=info_issuer["end_session_endpoint"],
            srv_discovery_url="{}/oauth2/oidcdiscovery/.well-known/openid-configuration".format(
                WS02_ISSUER
            ),
        )

        client.handle_provider_config(op_info, op_info["issuer"])

        info = {
            "client_id": settings.ws02_client_id,
            "client_secret": settings.ws02_client_secret,
        }

        client_reg = RegistrationResponse(**info)

        client.store_registration_info(client_reg)

        args = {
            "enabled": True,
            "authority": "{}/oauth2/oidcdiscovery/".format(WS02_ISSUER),
            "post_logout_redirect_uri": "{}".format(settings.url_frontend),
            "client_id": client.client_id,
            "response_type": ["code"],
            "scope": ["openid profile email"],
            "nonce": nonce,
            "redirect_uri": ["{}/oauth/logincallback".format(settings.url_backend)],
            "state": inner_state,
            "X-TRENA-KEY": settings.api_key,
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        print("FEZ REQUEST PRO WS02")
        return auth_req.request(client.authorization_endpoint)


class Wso2Router(BaseRouter):
    wso2_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.wso2_router

    @wso2_router.get("/authws02", response_class=HTMLResponse)
    def ws02(request: Request):
        print("REDIRECIONOU PARA A URL DE LOGIN DO WS02")
        return RedirectResponse(url=get_login_url())

    @wso2_router.get("/logoutcallback")
    def logout():
        return RedirectResponse(client.end_session_endpoint)

    @wso2_router.get(
        "/logincallback",
    )
    def callback(request: Request, db: Session = Depends(get_db)):
        print("FEZ AUTENTICAÇÃO COM O TRENA")
        params = request.query_params

        aresp = client.parse_response(
            AuthorizationResponse, info=str(params), sformat="urlencoded"
        )

        assert inner_state == aresp["state"]

        with no_ssl_verification():

            args = {"code": aresp["code"]}
            resp = client.do_access_token_request(
                state=aresp["state"],
                request_args=args,
                authn_method="client_secret_basic",
            )

        if resp["access_token"] != "":
            with no_ssl_verification():
                userinfo = client.do_user_info_request(
                    access_token=resp["access_token"], scope="profile"
                )

                print("DADOS DO WS02: {}".format(userinfo))

                user = repository.get_user_public_data_by_email(db, userinfo["email"])

                if user:
                    return user
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="No user with email: {} found.".format(
                            userinfo["email"]
                        ),
                    )

        else:
            raise HTTPException(status_code=400, detail="Failed to auth with Ws02")
