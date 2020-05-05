#!/usr/bin/env python3
from fastapi import FastAPI

mpApi = FastAPI()


@mpApi.get("/")
def read_root():
    return {"Hello": "World"}


@mpApi.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
