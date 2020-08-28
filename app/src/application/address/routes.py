from typing import List, Dict

import requests
from application.shared.base_router import BaseRouter

from fastapi import APIRouter, HTTPException, Depends, FastAPI
from sqlalchemy.orm import Session

from application.core.database import get_db
from application.core import config
from application.shared.response import Response, Error
from application.address.models.address import Address
from application.address.models.city import City

from application.address.database import repository


class AddressRouter(BaseRouter):
    address_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.address_router

    @staticmethod
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

    @staticmethod
    @address_router.post("/city/add")
    async def add_city(city: City, db: Session = Depends(get_db)) -> City:
        return repository.add_city(db, city)

    @staticmethod
    @address_router.post("/city/addAll")
    async def add_city(city: List[City], db: Session = Depends(get_db)) -> List[City]:
        return repository.add_cities(db, city)

    @staticmethod
    @address_router.get("/city/all")
    async def get_all_cities(db: Session = Depends(get_db)) -> List[City]:
        return repository.get_all_cities(db)

    @staticmethod
    @address_router.post("/city/delete")
    async def delete_city(codigo_ibge: str, db: Session = Depends(get_db)) -> Response:
        city_db = repository.delete_city(db, codigo_ibge)
        if city_db:
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Not able to delete city"))

    @staticmethod
    @address_router.get("/city/version")
    async def get_table_version(db: Session = Depends(get_db)) -> Dict[str, int]:
        return {"version": repository.get_city_table_version(db)}
