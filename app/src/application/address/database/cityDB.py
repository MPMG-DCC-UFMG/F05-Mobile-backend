from sqlalchemy import Column, Float, String

from application.core.database import Base
from application.address.models.city import City


class CityDB(Base):
    __tablename__ = "city"
    __versioned__ = {}

    codigo_ibge = Column(String, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    uf = Column(String, default="MG")

    @classmethod
    def from_model(cls, city: City):
        city_db = CityDB(
            codigo_ibge=city.codigo_ibge,
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude,
            uf=city.uf
        )

        return city_db
