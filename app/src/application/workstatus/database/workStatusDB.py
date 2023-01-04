from application.workstatus.models.workStatus import WorkStatus
from sqlalchemy import Column, Integer, String

from application.core.database import Base
from sqlalchemy.orm import relationship


class WorkStatusDB(Base):
    __tablename__ = "workstatus"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    type_works = relationship("TypeWorkDB", secondary='association_tw_ws')

    @classmethod
    def from_model(cls, work_status: WorkStatus):
        work_status_db = WorkStatusDB(
            name=work_status.name,
            description=work_status.description,
        )

        if work_status.flag != 0:
            work_status_db.flag = work_status.flag

        return work_status_db

    def parse_to_work_status(self):
        return WorkStatus(
            flag=self.flag,
            name=self.name,
            description=self.description,
        )

    def update(self, work_status: WorkStatus):
        self.flag = work_status.flag
        self.name = work_status.name
        self.description = work_status.description
