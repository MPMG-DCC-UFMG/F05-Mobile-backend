from typing import List, Dict

import requests

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.application.core.database import get_db
from src.application.core import config
from src.application.shared.response import Response, Error
from src.application.address.models.address import Address
from src.application.address.models.city import City

from src.application.address.database import repository

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


@address_router.post("/city/add")
async def add_city(city: City, db: Session = Depends(get_db)) -> City:
    return repository.add_city(db, city)


@address_router.get("/city/all")
async def get_all_cities(db: Session = Depends(get_db)) -> List[City]:
    return repository.get_all_cities(db)


@address_router.post("/city/delete")
async def delete_city(codigo_ibge: str, db: Session = Depends(get_db)) -> Response:
    city_db = repository.delete_city(db, codigo_ibge)
    if city_db:
        return Response(success=True)
    else:
        return Response(success=False, error=Error(status_code=401, message="Not able to delete city"))


@address_router.get("/city/version")
async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
    return {"version": repository.get_city_table_version(db)}
