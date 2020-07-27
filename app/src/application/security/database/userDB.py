from sqlalchemy import Column, Integer, String

from src.application.core.database import Base
from src.application.security.models.user import User


class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    full_name = Column(String)
    hashed_password = Column(String)

    @classmethod
    def from_model(cls, user: User):
        user_db = UserDB(
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.authentication
        )

        return user_db
