from pydantic.main import BaseModel


class City(BaseModel):
    codigo_ibge: str
    name: str
    latitude: float
    longitude: float
    uf: str
