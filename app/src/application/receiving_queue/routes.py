from typing import List

from application.collect.models.collect import Collect
from application.core.database import get_db
from application.photo.models.photo import Photo
from application.publicwork.models.publicwork import PublicWork
from application.receiving_queue.models.queue_item import QueueItem
from application.shared.base_router import BaseRouter
from application.shared.response import Response, Error
from fastapi import APIRouter, FastAPI, Depends, Query
import application.receiving_queue.data.repository as repository
from sqlalchemy.orm import Session


class QueueRouter(BaseRouter):
    queueRouter = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.queueRouter

    @staticmethod
    @queueRouter.post("/publicwork/add")
    async def add_public_work_to_queue(public_work: PublicWork) -> Response:
        if repository.add_public_work(public_work):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401,
                                                       message="Erro ao adicionar obra pública"))

    @staticmethod
    @queueRouter.post("/collect/add")
    async def add_collect_to_queue(collect: Collect, db: Session = Depends(get_db)) -> Response:
        if repository.add_collect(db, collect):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401,
                                                       message="Erro ao adicionar coleta a fila, obra pública não existe"))

    @staticmethod
    @queueRouter.post("/photo/add")
    async def add_photo_to_queue(photo: Photo, db: Session = Depends(get_db)) -> Response:
        if repository.add_photo(db, photo):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401,
                                                       message="Erro ao adicionar foto a fila, coleta não existe"))

    @staticmethod
    @queueRouter.get("/ids")
    async def get_all_ids() -> List[str]:
        return repository.list_collects_ids()

    @staticmethod
    @queueRouter.get("/items")
    async def get_all_queue_items(db: Session = Depends(get_db)) -> List[QueueItem]:
        return repository.list_queue_items(db)

    @staticmethod
    @queueRouter.get("/count")
    async def get_queue_count() -> int:
        return repository.queue_count()

    @staticmethod
    @queueRouter.post("/publicwork/{id}/accept")
    async def accept_public_work(id: str, db: Session = Depends(get_db)) -> Response:
        if repository.accept_public_work(db, id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao aceitar obra pública"))

    @staticmethod
    @queueRouter.post("/publicwork/{id}/delete")
    async def delete_public_work(id: str) -> Response:
        if repository.delete_public_work(id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao deletar obra pública"))

    @staticmethod
    @queueRouter.post("/publicwork/{public_work_id}/collect/{collect_id}/accept")
    async def accept_collect(public_work_id: str, collect_id: str, db: Session = Depends(get_db)) -> Response:
        if repository.accept_collect(db, public_work_id, collect_id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao aceitar coleta"))

    @staticmethod
    @queueRouter.post("/publicwork/{public_work_id}/collect/{collect_id}/delete")
    async def delete_collect(public_work_id: str, collect_id: str) -> Response:
        if repository.delete_collect(public_work_id, collect_id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao deletar coleta"))

    @staticmethod
    @queueRouter.get("/publicwork/{public_work_id}/collect/{collect_id}/photos")
    async def get_photos_of_collect(public_work_id: str, collect_id: str) -> List[Photo]:
        return repository.get_photos_of_collect(public_work_id, collect_id)

    @staticmethod
    @queueRouter.get("/publicwork/{public_work_id}/collects")
    async def get_collects_of_public_work(public_work_id: str) -> List[Collect]:
        return repository.list_collects_of_public_work(public_work_id)

    @staticmethod
    @queueRouter.get("/publicwork/{public_work_id}")
    async def get_public_work(public_work_id: str) -> PublicWork:
        return repository.get_public_work(public_work_id)

    @staticmethod
    @queueRouter.post("/publicwork/{public_work_id}/photo/{photo_id}/accept")
    async def accept_photo(public_work_id: str, photo_id: str, db: Session = Depends(get_db)) -> Response:
        if repository.accept_photo(db, public_work_id, photo_id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao aceitar foto"))

    @staticmethod
    @queueRouter.post("/publicwork/{public_work_id}/photo/{photo_id}/delete")
    async def delete_photo(public_work_id: str, photo_id: str, db: Session = Depends(get_db)) -> Response:
        if repository.deletePhoto(db, public_work_id, photo_id):
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Erro ao deletar foto"))
