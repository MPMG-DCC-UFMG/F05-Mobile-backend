from pydantic import BaseModel


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
