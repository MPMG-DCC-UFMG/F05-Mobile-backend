from sqlalchemy.orm import Session

from src.application.address.models.address import Address
from src.application.address.database.addressDB import AddressDB


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
