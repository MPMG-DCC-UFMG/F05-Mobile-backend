from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette.requests import Request

from src.application.image.database import repository
from src.application.core import config

images_router = APIRouter()


@images_router.post("/upload", responses={403: {"description": "Operation forbidden"}})
def upload_image(request: Request, file: UploadFile = File(...)):
    image_folder = config.settings.image_folder
    saved = repository.save_upload_file(file, Path(image_folder))
    if saved:
        filepath = "{0}{1}{2}".format(request.base_url.__str__(), "images/", file.filename)
        return {"filepath": filepath}
    else:
        raise HTTPException(status_code=403, detail="Not able to find public work to delete")


@images_router.get("/")
async def get_image(image_name: str) -> FileResponse:
    file_path = "{0}{1}".format(config.settings.image_folder, image_name)
    return FileResponse(file_path)
