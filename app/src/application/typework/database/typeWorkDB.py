from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from application.core.database import Base
from application.typework.models.typeWork import TypeWork


class TypeWorkDB(Base):
    __tablename__ = "typework"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    public_works = relationship("PublicWorkDB", backref="typework", cascade="all, delete-orphan")

    type_photos = relationship("TypePhotoDB", secondary='association_type_ph_pw')
    work_statuses = relationship("WorkStatusDB", secondary='association_tw_ws')

    @classmethod
    def from_model(cls, type_work: TypeWork):
        type_work_db = TypeWorkDB(name=type_work.name)

        if type_work.flag != 0:
            type_work_db.flag = type_work.flag

        return type_work_db

    def parse_to_type_work(self):
        parsed_list = []
        if len(self.work_statuses) > 0:
            parsed_list = list(map(lambda work_status: work_status.flag, self.work_statuses))
        return TypeWork(
            flag=self.flag,
            name=self.name,
            status_list=parsed_list
        )

    def update(self, type_work: TypeWork):
        self.flag = type_work.flag
        self.name = type_work.name
