from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship, backref
from src.application.core.database import Base
from src.application.core.helpers import generate_uuid
from src.application.publicwork.models.publicwork import PublicWork


class PublicWorkDB(Base):
    __tablename__ = "publicwork"
    __versioned__ = {}

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String)
    type_work_flag = Column(Integer, ForeignKey("typework.flag"))
    address = relationship("AddressDB", backref=backref("publicwork", uselist=False))

    def update(self, public_work: PublicWork):
        self.name = public_work.name
        self.id = public_work.id
        self.type_work_flag = public_work.type_work_flag
