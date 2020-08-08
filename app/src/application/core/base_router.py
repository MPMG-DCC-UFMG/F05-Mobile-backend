from abc import abstractmethod
from typing import List

from fastapi import FastAPI, APIRouter, Depends


class BaseRouter:

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        self.prefix = prefix
        self.app = app
        self.dependencies = dependencies

    @abstractmethod
    def route(self) -> APIRouter:
        pass

    def apply_route(self):
        dependencies = self.dependencies
        if self.dependencies is None:
            dependencies = []
        self.app.include_router(self.route(), prefix="/" + self.prefix,
                                tags=[self.prefix],
                                responses={404: {"description": "{0} not found".format(self.prefix)}},
                                dependencies=dependencies)
