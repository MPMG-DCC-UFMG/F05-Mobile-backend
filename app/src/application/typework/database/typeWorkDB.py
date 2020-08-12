from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from application.core.database import Base
from application.typework.models.typeWork import TypeWork


class TypeWorkDB(Base):
    __tablename__ = "typework"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    status_list = Column(String)

    public_works = relationship("PublicWorkDB", backref="typework", cascade="all, delete-orphan")

    @classmethod
    def from_model(cls, type_work: TypeWork):
        parsed_list = ",".join(map(str, type_work.status_list))
        type_work_db = TypeWorkDB(
            name=type_work.name,
            status_list=parsed_list)

        if type_work.flag != 0:
            type_work_db.flag = type_work.flag

        return type_work_db

    def parse_to_type_work(self):
        parsed_list = list(map(int, self.status_list.split(',')))
        return TypeWork(
            flag=self.flag,
            name=self.name,
            status_list=parsed_list
        )

    def update(self, type_work: TypeWork):
        parsed_list = ",".join(map(str, type_work.status_list))
        self.flag = type_work.flag
        self.name = type_work.name
        self.status_list = parsed_list
