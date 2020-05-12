from pydantic import BaseModel
from src.application.address.database.addressDB import AddressDB
from src.application.core.helpers import is_valid_uuid


class Address(BaseModel):
    id: str = None
    street: str
    neighborhood: str
    number: str
    latitude: float
    longitude: float
    city: str
    state: str = "MG"
    cep: str

    class Config:
        orm_mode = True

    def to_db(self) -> AddressDB:
        address_db = AddressDB(
            street=self.street,
            neighborhood=self.neighborhood,
            number=self.number,
            latitude=self.latitude,
            longitude=self.longitude,
            city=self.city,
            state=self.state,
            cep=self.cep
        )

        if id and is_valid_uuid(id):
            address_db.id = self.id

        return address_db
