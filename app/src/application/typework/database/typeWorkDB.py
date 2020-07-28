from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from application.core.database import Base
from application.typework.models.typeWork import TypeWork


class TypeWorkDB(Base):
    __tablename__ = "typework"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    public_works = relationship("PublicWorkDB", backref="typework", cascade="all, delete-orphan")

    def update(self, type_work: TypeWork):
        self.flag = type_work.flag
        self.name = type_work.name


