from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from application.core.database import Base
from application.inspection.models.inspection import Inspection


class InspectionDB(Base):
    __tablename__ = "inspection"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    public_work_id = Column(String)
    collect_id = Column(String)
    status = Column(Integer)

    @classmethod
    def from_model(cls, inspection: Inspection):
        inspection_db = InspectionDB(name=inspection.name, description=inspection.description, public_work_id=inspection.public_work_id, collect_id=inspection.collect_id, status=inspection.status)
        return inspection_db

    def parse_to_inspect(self):
        return Inspection(
            flag=self.flag,
            name=self.name,
            description=self.description,
            public_work_id=self.public_work_id,
            collect_id=self.collect_id,
            status=self.status
        )

    def update(self, inspection: Inspection):
        self.flag = inspection.flag
        self.name = inspection.name
        self.description = inspection.description
        self.public_work_id = inspection.public_work_id
        self.collect_id = inspection.collect_id
        self.status = inspection.status
