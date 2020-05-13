from sqlalchemy import Column, Float, String, ForeignKey

from sqlalchemy.orm import relationship

from src.application.core.database import Base
from src.application.core.helpers import generate_uuid


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


