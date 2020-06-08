import shutil

from pathlib import Path

from fastapi import UploadFile


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
