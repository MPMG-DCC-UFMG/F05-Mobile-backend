from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from sqlalchemy.orm import relationship, backref
from application.core.database import Base
from application.inspection.models.inspection import Inspection
from application.calendar.calendar_utils import get_today


class InspectionDB(Base):
    __tablename__ = "inspection"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    inquire_number = Column(Integer)
    description = Column(String)
    public_work_id = Column(String, ForeignKey("publicwork.id"))
    collect_id = Column(String)
    status = Column(Integer)
    user_email = Column(String)
    request_date = Column(BigInteger, default=get_today())
    timestamp = Column(BigInteger, default=get_today())
    # user_id = Column(String, ForeignKey("user.id"))

    # user = relationship(
    #     "UserDB",
    #     backref=backref("inspection", cascade="all,delete-orphan", uselist=False),
    #     lazy=False,
    #     foreign_keys=[user_id],
    # )

    @classmethod
    def from_model(cls, inspection: Inspection):
        inspection_db = InspectionDB(
            flag=inspection.flag,
            name=inspection.name,
            inquire_number=inspection.inquire_number,
            description=inspection.description,
            public_work_id=inspection.public_work_id,
            collect_id=inspection.collect_id,
            status=inspection.status,
            user_email=inspection.user_email,
            request_date=inspection.request_date,
        )
        return inspection_db

    def parse_to_inspect(self):
        return Inspection(
            flag=self.flag,
            name=self.name,
            inquire_number=self.inquire_number,
            description=self.description,
            public_work_id=self.public_work_id,
            collect_id=self.collect_id,
            status=self.status,
            user_email=self.user_email,
            request_date=self.request_date,
        )

    def update(self, inspection: Inspection):
        self.flag = inspection.flag
        self.name = inspection.name
        self.inquire_number = inspection.inquire_number
        self.description = inspection.description
        self.public_work_id = inspection.public_work_id
        self.collect_id = inspection.collect_id
        self.status = inspection.status
        self.user_email = inspection.user_email
        self.request_date = inspection.request_date
