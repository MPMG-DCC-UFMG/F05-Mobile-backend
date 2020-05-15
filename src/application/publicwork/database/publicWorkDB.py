from sqlalchemy import Column, Integer, String, ForeignKey
from src.application.address.database.addressDB import AddressDB

from sqlalchemy.orm import relationship, backref
from src.application.core.database import Base
from src.application.core.helpers import generate_uuid


class PublicWorkDB(Base):
    __tablename__ = "publicwork"
    __versioned__ = {}

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String)
    type_work_flag = Column(Integer, ForeignKey("typework.flag"))
    address_id = Column(String, ForeignKey("address.id"))

    address = relationship("AddressDB", backref=backref("publicwork", uselist=False), lazy=False)
