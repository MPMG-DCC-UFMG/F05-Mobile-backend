import shutil

from pathlib import Path
from application.core import config
from application.file.file_utils import check_folder_exists_or_create

from fastapi import UploadFile


def check_folder_exists():
    check_folder_exists_or_create(config.settings.image_folder)


def save_upload_file(upload_file: UploadFile, destination: Path) -> bool:
    destination = destination.joinpath(upload_file.filename)
    file_saved = True
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception:
        file_saved = False
    finally:
        upload_file.file.close()

    return file_saved
