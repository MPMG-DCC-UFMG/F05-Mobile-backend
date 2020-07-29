from sqlalchemy import Column, Float, String

from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.address.models.address import Address


class AddressDB(Base):
    __tablename__ = "address"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    street = Column(String)
    neighborhood = Column(String)
    number = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
    state = Column(String, default="MG")
    cep = Column(String)
    public_work_id = Column(String)

    @classmethod
    def from_model(cls, address: Address):
        address_db = AddressDB(
            street=address.street,
            neighborhood=address.neighborhood,
            number=address.number,
            latitude=address.latitude,
            longitude=address.longitude,
            city=address.city,
            state=address.state,
            cep=address.cep,
            public_work_id=address.public_work_id
        )

        if address.id and is_valid_uuid(address.id):
            address_db.id = address.id

        return address_db

    def update(self, address: Address):
        self.id = address.id
        self.street = address.street
        self.state = address.state
        self.number = address.number
        self.neighborhood = address.neighborhood
        self.latitude = address.latitude
        self.longitude = address.longitude
        self.city = address.city
        self.cep = address.cep
        self.public_work_id = address.public_work_id
