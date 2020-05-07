from sqlalchemy import Column, Integer, String
from src.application.core.database import Base


class TypeWorkDB(Base):
    __tablename__ = "typework"

    flag = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
