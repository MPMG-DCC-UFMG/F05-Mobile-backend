import json
from pathlib import Path
from typing import List

from application.core import config
from pydantic import BaseModel


def check_folder_exists_or_create(folder: str):
    Path(folder).mkdir(parents=True, exist_ok=True)

def create_json_file(data: BaseModel):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def create_json_file_from_list(filename: str, data: List[BaseModel]) -> Path:
    report_folder = Path(config.settings.report_folder)
    check_folder_exists_or_create(report_folder)
    destination = report_folder.joinpath(filename + ".json")
    new_data = list(map(lambda item: item.json(), data))
    with destination.open('w') as outfile:
        json.dump(new_data, outfile, indent=4, sort_keys=True)
    return destination.absolute()

