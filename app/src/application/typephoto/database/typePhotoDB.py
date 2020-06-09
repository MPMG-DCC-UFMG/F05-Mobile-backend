from sqlalchemy import Column, Integer, String

from src.application.core.database import Base

from src.application.typephoto.models.typePhoto import TypePhoto


class TypePhotoDB(Base):
    __tablename__ = "typephoto"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    def update(self, type_photo: TypePhoto):
        self.flag = type_photo.flag
        self.name = type_photo.name
