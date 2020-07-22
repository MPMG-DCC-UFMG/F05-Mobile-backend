from sqlalchemy import Column, Integer, ForeignKey
from src.application.core.database import Base


class AssociationTypePhPWDB(Base):
    __tablename__ = "association_type_ph_pw"
    __versioned__ = {}

    type_work_flag = Column(Integer, ForeignKey("typework.flag"), primary_key=True)
    type_photo_flag = Column(Integer, ForeignKey("typephoto.flag"), primary_key=True)
