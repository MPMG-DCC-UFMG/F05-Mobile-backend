from sqlalchemy import Column, BigInteger, String, ForeignKey, Integer

from sqlalchemy.orm import relationship

from application.core.database import Base
from application.core.helpers import generate_uuid, is_valid_uuid

from application.collect.models.collect import Collect


class CollectDB(Base):
    __tablename__ = "collect"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    date = Column(BigInteger)
    comments = Column(String)
    user_email = Column(String)
    public_work_status = Column(Integer)

    public_work_id = Column(String, ForeignKey("publicwork.id"))
    inspection_flag = Column(String, ForeignKey("inspection.flag"), nullable=True)

    photos = relationship("PhotoDB", cascade="all,delete-orphan", backref="photo")

    @classmethod
    def from_model(cls, collect: Collect):
        collect_db = CollectDB(
            date=collect.date,
            comments=collect.comments,
            public_work_id=collect.public_work_id,
            inspection_flag=collect.inspection_flag if collect.inspection_flag != "" else None,
            user_email=collect.user_email,
            public_work_status=collect.public_work_status
        )

        if collect.id and is_valid_uuid(collect.id):
            collect_db.id = collect.id

        return collect_db

    def parse_to_collect(self):
        return Collect(
            id=self.id,
            public_work_id=self.public_work_id,
            inspection_flag=self.inspection_flag,
            date=self.date,
            user_email=self.user_email,
            comments=self.comments,
            public_work_status=self.public_work_status,
            photos=self.photos
        )

    def update(self, collect: Collect):
        self.id = collect.id
        self.comments = collect.comments
        self.public_work_id = collect.public_work_id
        self.inspection_flag = collect.inspection_flag
        self.user_email = collect.user_email
        self.date = collect.date
        self.public_work_status = collect.public_work_status
