from sqlalchemy import Column, Integer, String
from src.application.core.database import Base
from src.application.typework.models.typeWork import TypeWork


class TypeWorkDB(Base):
    __tablename__ = "typework"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def update(self, type_work: TypeWork):
        self.flag = type_work.flag
        self.name = type_work.name
