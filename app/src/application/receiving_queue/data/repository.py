from typing import List, Optional

from application.collect.database.collectDB import CollectDB
from application.collect.models.collect import Collect
from application.photo.database.photoDB import PhotoDB
from application.photo.models.photo import Photo
from application.publicwork.models.publicwork import PublicWork
from application.receiving_queue.data.database import QueueDB

import application.publicwork.database.repository as publicwork_repository
import application.address.database.repository as address_repository
import application.collect.database.repository as collect_repository
import application.photo.database.repository as photo_repository
from application.receiving_queue.models.queue_item import QueueItem

from sqlalchemy.orm import Session

DATA_ID_KEY = "data.id"

db = QueueDB.database()


def add_public_work(public_work: PublicWork) -> bool:
    db[public_work.id].replace_one(
        {DATA_ID_KEY: public_work.id},
        {"type": "publicwork", "data": public_work.dict()},
        upsert=True)
    return True


def add_collect(sqldb: Session, collect: Collect) -> bool:
    if collect.public_work_id in db.list_collection_names() \
            or publicwork_repository.get_public_work_by_id(sqldb, collect.public_work_id):
        db[collect.public_work_id].replace_one(
            {DATA_ID_KEY: collect.id},
            {"type": "collect", "data": collect.dict()},
            upsert=True)
        return True
    else:
        return False


def has_collect(sqldb: Session, collect_id: str) -> Optional[Collect]:
    for name in db.list_collection_names():
        found = db[name].find_one({"type": "collect", DATA_ID_KEY: collect_id})
        if found:
            return Collect.parse_obj(found['data'])
    found = collect_repository.get_collect_by_id(sqldb, collect_id)
    return found


def get_public_work(public_work_id: str) -> Optional[PublicWork]:
    public_work = PublicWork.parse_obj(db[public_work_id].find_one({"type": "publicwork"}))
    if public_work:
        return PublicWork.parse_obj(public_work['data'])
    else:
        return None


def add_photo(sqldb: Session, photo: Photo) -> bool:
    collect = has_collect(sqldb, photo.collect_id)
    if collect:
        db[collect.public_work_id].replace_one(
            {DATA_ID_KEY: photo.id},
            {"type": "photo", "data": photo.dict()},
            upsert=True)
        return True
    else:
        return False


def get_collect_public_work(sqldb: Session, public_work_id: str) -> PublicWork:
    public_work = db[public_work_id].find_one({"type": "publicwork"})
    if not public_work:
        public_work = publicwork_repository.get_public_work_by_id(sqldb, public_work_id)
    else:
        public_work = PublicWork.parse_obj(public_work['data'])
    return public_work


def list_collects_of_public_work(public_work_id: str) -> List[Collect]:
    queue = db[public_work_id].find({"type": "collect"})
    result = []
    for q in queue:
        collect = Collect.parse_obj(q['data'])
        photos = db[public_work_id].find({"type": "photo", 'data.collect_id': collect.id})
        collect.photos = list(map(lambda photo: Photo.parse_obj(photo['data']), photos))
        result.append(collect)
    return result


def list_public_work_names(sqldb: Session) -> List[str]:
    ids = db.list_collection_names()
    names = []
    for public_work_id in ids:
        public_work = get_collect_public_work(sqldb, public_work_id)
        names.append(public_work.name)
    return names


def list_queue_items(sqldb: Session) -> List[QueueItem]:
    ids = db.list_collection_names()
    queue_items = []
    for public_work_id in ids:
        public_work = get_collect_public_work(sqldb, public_work_id)
        queue_item = QueueItem(
            public_work=public_work,
            public_work_count=db[public_work_id].find({"type": "publicwork"}).count(),
            collect_count=db[public_work_id].find({"type": "collect"}).count(),
            photo_count=db[public_work_id].find({"type": "photo"}).count(),
        )
        queue_items.append(queue_item)
    return queue_items


def queue_count() -> int:
    return len(db.list_collection_names())


def list_collects_ids() -> List[str]:
    names = db.list_collection_names()
    return names


def accept_public_work(sqldb: Session, public_work_id: str) -> bool:
    public_work = db[public_work_id].find_one({"type": "publicwork"})
    if public_work:
        parsed = PublicWork.parse_obj(public_work['data'])

        if address_repository.upsert_address(sqldb, parsed.address) \
                and publicwork_repository.upsert_public_work(sqldb, parsed):
            db[public_work_id].delete_one({"type": "publicwork"})
            check_collection_empty(public_work_id)
            return True
        return False
    else:
        return False


def delete_public_work(public_work_id: str) -> bool:
    db[public_work_id].drop()


def accept_collect(sqldb: Session, public_work_id: str, collect_id: str) -> bool:
    collect = db[public_work_id].find_one({"type": "collect", DATA_ID_KEY: collect_id})
    if collect:
        parsed = Collect.parse_obj(collect['data'])
        if collect_repository.add_collect(sqldb, parsed):
            db[public_work_id].delete_many({"type": "collect", DATA_ID_KEY: collect_id})
            check_collection_empty(public_work_id)
            return True
        return False
    else:
        return False


def delete_collect(public_work_id: str, collect_id: str) -> bool:
    collect = db[public_work_id].find_one({"type": "collect", DATA_ID_KEY: collect_id})
    if collect:
        db[public_work_id].delete_many({"type": "collect", DATA_ID_KEY: collect_id})
        db[public_work_id].delete_many({"type": "photo", 'data.collect_id': collect_id})
        check_collection_empty(public_work_id)
        return True
    return False


def accept_photo(sqldb: Session, public_work_id: str, photo_id: str) -> bool:
    photo = db[public_work_id].find_one({"type": "photo", DATA_ID_KEY: photo_id})
    if photo:
        parsed = Photo.parse_obj(photo['data'])
        if photo_repository.add_photo(sqldb, parsed):
            db[public_work_id].delete_many({"type": "photo", DATA_ID_KEY: photo_id})
            check_collection_empty(public_work_id)
            return True
        return False
    return False


def deletePhoto(public_work_id: str, photo_id: str) -> bool:
    photo = db[public_work_id].find_one({"type": "photo", DATA_ID_KEY: photo_id})
    if photo:
        db[public_work_id].delete_many({"type": "photo", DATA_ID_KEY: photo_id})
        check_collection_empty(public_work_id)
        return True
    return False


def check_collection_empty(public_work_id: str):
    if db[public_work_id].count() == 0:
        db[public_work_id].drop()


def get_photos_of_collect(public_work_id: str, collect_id: str) -> List[Photo]:
    photos = db[public_work_id].find({"type": "photo", "data.collect_id": collect_id})
    return list(map(lambda photo: Photo.parse_obj(photo['data']), photos))
