import requests
from application.core.config import settings
from application.security.database import repository
from application.ws02.utils.network import no_ssl_verification
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from oic import rndstr
from oic.oic import Client
from oic.oic.message import (
    AuthorizationResponse,
    ProviderConfigurationResponse,
    RegistrationResponse,
)
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from sqlalchemy.orm import Session

inner_state = rndstr()
nonce = rndstr()
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)


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
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        url = auth_req.request(client.authorization_endpoint)
        return url


def get_user_info(params, db: Session):
    aresp = client.parse_response(AuthorizationResponse, info=params, sformat="dict")

    assert inner_state == aresp["state"]

    with no_ssl_verification():

        args = {"code": aresp["code"]}
        resp = client.do_access_token_request(
            state=aresp["state"],
            request_args=args,
            authn_method="client_secret_basic",
        )

        assert resp["access_token"] != "", "Could not retrieve WS02 access token"

        userinfo = client.do_user_info_request(
            access_token=resp["access_token"], scope="profile"
        )

        user = repository.get_user_public_data_by_email(db, userinfo["email"])

        if user:
            return RedirectResponse(settings.url_frontend)
        else:
            raise HTTPException(
                status_code=400,
                detail="No user with email: {} found.".format(userinfo["email"]),
            )
