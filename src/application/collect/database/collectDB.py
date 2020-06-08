from sqlalchemy import Column, BigInteger, String, ForeignKey

from sqlalchemy.orm import relationship

from src.application.core.database import Base
from src.application.core.helpers import generate_uuid


class CollectDB(Base):
    __tablename__ = "collect"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    date = Column(BigInteger)
    comments = Column(String)
    user_email = Column(String)

    public_work_id = Column(String, ForeignKey("publicwork.id"))

    photos = relationship("PhotoDB", backref="photo")
