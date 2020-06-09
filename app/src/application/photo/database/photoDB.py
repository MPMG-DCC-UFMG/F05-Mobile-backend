from sqlalchemy import Column, Float, String, BigInteger, ForeignKey

from src.application.core.database import Base
from src.application.core.helpers import generate_uuid


class PhotoDB(Base):
    __tablename__ = "photo"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    filepath = Column(String)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    comment = Column(String)
    timestamp = Column(BigInteger)

    collect_id = Column(String, ForeignKey("collect.id"))
