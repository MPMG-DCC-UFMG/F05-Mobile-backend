from application.core.database import Base
from sqlalchemy import Column, Integer, ForeignKey


class AssociationTWWSDB(Base):
    __tablename__ = "association_tw_ws"
    __versioned__ = {}

    type_work_flag = Column(Integer, ForeignKey("typework.flag"), primary_key=True)
    work_status_flag = Column(Integer, ForeignKey("workstatus.flag"), primary_key=True)
