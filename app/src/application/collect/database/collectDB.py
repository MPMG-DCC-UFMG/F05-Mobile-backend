from sqlalchemy import Column, BigInteger, String, ForeignKey

from sqlalchemy.orm import relationship

from src.application.core.database import Base
from src.application.core.helpers import generate_uuid, is_valid_uuid

from src.application.collect.models.collect import Collect


class CollectDB(Base):
    __tablename__ = "collect"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    date = Column(BigInteger)
    comments = Column(String)
    user_email = Column(String)

    public_work_id = Column(String, ForeignKey("publicwork.id"))

    photos = relationship("PhotoDB", backref="photo")

    @classmethod
    def from_model(cls, collect: Collect):
        collect_db = CollectDB(
            date=collect.date,
            comments=collect.comments,
            public_work_id=collect.public_work_id,
            user_email=collect.user_email
        )

        if collect.id and is_valid_uuid(collect.id):
            collect_db.id = collect.id

        return collect_db

    def update(self, collect: Collect):
        self.id = collect.id
        self.comments = collect.comments
        self.public_work_id = collect.public_work_id
        self.user_email = collect.user_email
        self.date = collect.date