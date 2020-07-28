from typing import List

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy_continuum import version_class

from application.address.models.address import Address
from application.address.database.addressDB import AddressDB

from application.address.models.city import City
from application.address.database.cityDB import CityDB


def get_address_by_id(db: Session, address_id) -> Address:
    return db.query(AddressDB).filter(AddressDB.id == address_id).first()


def add_address(db: Session, address: Address) -> Address:
    db_address = AddressDB.from_model(address)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def update_address(db: Session, address: Address) -> Address:
    db_address = db.query(AddressDB).filter(AddressDB.id == address.id).first()
    if db_address:
        db_address.update(address)
        db.commit()
        db.refresh(db_address)
        return db_address


def upsert_address(db: Session, address: Address) -> Address:
    db_address = update_address(db, address)
    if db_address:
        return db_address
    else:
        return add_address(db, address)


def delete_address(db: Session, address_id: str) -> Address:
    db_address = db.query(AddressDB).filter(AddressDB.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address


def get_city_table_version(db: Session) -> int:
    version = version_class(CityDB)
    last_changed = db.query(version).order_by(desc(version.transaction_id)).limit(1)
    if last_changed.count() > 0:
        return last_changed[0].transaction_id
    else:
        return -1


def add_city(db: Session, city: City) -> City:
    db_city = CityDB.from_model(city)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session) -> List[City]:
    return db.query(CityDB).all()


def delete_city(db: Session, codigo_ibge: str) -> City:
    db_city = db.query(CityDB).filter(CityDB.codigo_ibge == codigo_ibge).first()
    if db_city:
        db.delete(db_city)
        db.commit()
    return db_city
