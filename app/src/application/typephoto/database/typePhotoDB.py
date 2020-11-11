from sqlalchemy import Column, Integer, String

from application.core.database import Base

from application.typephoto.models.typePhoto import TypePhoto
from sqlalchemy.orm import relationship


class TypePhotoDB(Base):
    __tablename__ = "typephoto"
    __versioned__ = {}

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)

    type_works = relationship("TypeWorkDB", secondary='association_type_ph_pw')

    @classmethod
    def from_model(cls, type_photo: TypePhoto):
        type_photo_db = TypePhotoDB(
            name=type_photo.name,
            description=type_photo.description)

        if type_photo.flag != 0:
            type_photo_db.flag = type_photo.flag

        return type_photo_db

    def update(self, type_photo: TypePhoto):
        self.flag = type_photo.flag
        self.name = type_photo.name
        self.description = type_photo.description
