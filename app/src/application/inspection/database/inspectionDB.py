from application.calendar.calendar_utils import get_today
from application.core.database import Base
from application.inspection.models.inspection import Inspection
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship


class InspectionDB(Base):
    __tablename__ = "inspection"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    inquiry_number = Column(Integer)
    description = Column(String)
    collect_id = Column(String)
    status = Column(Integer)
    request_date = Column(BigInteger, default=get_today())
    timestamp = Column(BigInteger, default=get_today())
    secret = Column(Boolean, default=False)

    public_work_id = Column(String, ForeignKey("publicwork.id"))
    user_email = Column(String, ForeignKey("user.email"))

    @classmethod
    def from_model(cls, inspection: Inspection):
        inspection_db = InspectionDB(
            flag=inspection.flag,
            name=inspection.name,
            inquiry_number=inspection.inquiry_number,
            description=inspection.description,
            public_work_id=inspection.public_work_id,
            collect_id=inspection.collect_id,
            status=inspection.status,
            user_email=inspection.user_email,
            request_date=inspection.request_date,
            secret=inspection.secret,
        )
        return inspection_db

    def parse_to_inspect(self):
        return Inspection(
            flag=self.flag,
            name=self.name,
            inquiry_number=self.inquiry_number,
            description=self.description,
            public_work_id=self.public_work_id,
            collect_id=self.collect_id,
            status=self.status,
            user_email=self.user_email,
            request_date=self.request_date,
            secret=self.secret,
        )

    def update(self, inspection: Inspection):
        self.flag = inspection.flag
        self.name = inspection.name
        self.inquiry_number = inspection.inquiry_number
        self.description = inspection.description
        self.public_work_id = inspection.public_work_id
        self.collect_id = inspection.collect_id
        self.status = inspection.status
        self.user_email = inspection.user_email
        self.request_date = inspection.request_date
        self.secret = inspection.secret
