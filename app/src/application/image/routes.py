from pathlib import Path
from typing import List

from application.shared.base_router import BaseRouter
from fastapi import APIRouter, UploadFile, File, HTTPException, FastAPI, Depends
from fastapi.responses import FileResponse
from starlette.requests import Request
from application.security.core.api_key import get_api_key

from application.image.database import repository
from application.core import config


class ImageRouter(BaseRouter):
    images_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.images_router

    @staticmethod
    @images_router.post("/upload", dependencies=[Depends(get_api_key)], responses={403: {"description": "Operation forbidden"}})
    def upload_image(request: Request, file: UploadFile = File(...)):
        repository.check_folder_exists()
        image_folder = config.settings.image_folder
        saved = repository.save_upload_file(file, Path(image_folder))
        if saved:
            filepath = "{0}{1}{2}".format(request.base_url.__str__(), "images/", file.filename)
            return {"filepath": filepath}
        else:
            raise HTTPException(status_code=403, detail="Not able to add image")

    @staticmethod
    @images_router.get("/{image_name}")
    async def get_image(image_name: str) -> FileResponse:
        file_path = "{0}{1}".format(config.settings.image_folder, image_name)
        return FileResponse(file_path)
