from application.workstatus.models.workStatus import WorkStatus
from sqlalchemy import Column, Integer, String

from application.core.database import Base


class WorkStatusDB(Base):
    __tablename__ = "workstatus"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    type_work_list = Column(String)

    @classmethod
    def from_model(cls, work_status: WorkStatus):
        parsed_list = ",".join(map(str, work_status.type_work_list))
        work_status_db = WorkStatusDB(
            name=work_status.name,
            description=work_status.description,
            type_work_list=parsed_list
        )

        if work_status.flag != 0:
            work_status_db.flag = work_status.flag

        return work_status_db

    def parse_to_work_status(self):
        parsed_list = []
        if len(self.type_work_list) > 0:
            parsed_list = list(map(int, self.type_work_list.split(',')))
        return WorkStatus(
            flag=self.flag,
            name=self.name,
            description=self.description,
            type_work_list=parsed_list
        )

    def update(self, work_status: WorkStatus):
        parsed_list = ",".join(map(str, work_status.type_work_list))
        self.flag = work_status.flag
        self.name = work_status.name
        self.description = work_status.description
        self.type_work_list = parsed_list
