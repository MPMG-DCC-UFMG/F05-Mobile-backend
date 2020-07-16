import requests

from fastapi import APIRouter, HTTPException
from src.application.core import config
from src.application.address.models.address import Address

address_router = APIRouter()


@address_router.get("/by_cep/")
async def get_address_by_cep(cep: str) -> Address:
    url = "https://www.cepaberto.com/api/v3/cep?cep={0}".format(cep)
    headers = {'Authorization': 'Token token={0}'.format(config.settings.token_cep_aberto)}
    try:
        response = requests.get(url, headers=headers)
        parsed_response = response.json()
        address = Address(
            street=parsed_response["logradouro"],
            neighborhood=parsed_response["bairro"],
            number="",
            latitude=parsed_response["latitude"],
            longitude=parsed_response["longitude"],
            city=parsed_response["cidade"]["nome"],
            state="MG",
            cep=cep,
            public_work_id=None
        )
        return address
    except Exception:
        raise HTTPException(status_code=4005, detail="Error in parsing result or invalid CPF")
