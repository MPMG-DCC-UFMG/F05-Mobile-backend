from sqlalchemy import Column, Integer, String, ForeignKey
from application.address.database.addressDB import AddressDB
from application.collect.database.collectDB import CollectDB

from sqlalchemy.orm import relationship, backref
from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.publicwork.models.publicwork import PublicWork


class PublicWorkDB(Base):
    __tablename__ = "publicwork"
    __versioned__ = {}

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String)
    type_work_flag = Column(Integer, ForeignKey("typework.flag"))
    address_id = Column(String, ForeignKey("address.id"))
    user_status = Column(Integer)
    rnn_status = Column(Integer)

    address = relationship("AddressDB", backref=backref("publicwork", cascade="all,delete-orphan", uselist=False),
                           lazy=False, foreign_keys=[address_id])
    collect = relationship("CollectDB")

    @classmethod
    def from_model(cls, public_work: PublicWork):
        public_work_db = PublicWorkDB(
            name=public_work.name,
            type_work_flag=public_work.type_work_flag,
            address_id=public_work.address.id,
            user_status=public_work.user_status
        )

        if public_work.id and is_valid_uuid(public_work.id):
            public_work_db.id = public_work.id

        return public_work_db

    def update(self, public_work: PublicWork):
        self.id = public_work.id
        self.name = public_work.name
        self.type_work_flag = public_work.type_work_flag
        self.address_id = public_work.address.id
        if public_work.rnn_status:
            self.rnn_status = public_work.rnn_status
        self.user_status = public_work.user_status
