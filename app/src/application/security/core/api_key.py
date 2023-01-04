from application.core import config
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

API_KEY = config.settings.api_key
API_KEY_NAME = "X-TRENA-KEY"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )



 