from fastapi import FastAPI
from . import config

mpApi = FastAPI()


@mpApi.get("/")
def read_root():
    return {"Hello": "World"}


@mpApi.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
