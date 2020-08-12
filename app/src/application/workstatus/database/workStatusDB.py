from application.workstatus.models.workStatus import WorkStatus
from sqlalchemy import Column, Integer, String

from application.core.database import Base


class WorkStatusDB(Base):
    __tablename__ = "workstatus"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    @classmethod
    def from_model(cls, work_status: WorkStatus):
        work_status_db = WorkStatusDB(
            name=work_status.name,
            description=work_status.description)

        if work_status.flag != 0:
            work_status_db.flag = work_status.flag

        return work_status_db

    def update(self, work_status: WorkStatus):
        self.flag = work_status.flag
        self.name = work_status.name
        self.description = work_status.description
