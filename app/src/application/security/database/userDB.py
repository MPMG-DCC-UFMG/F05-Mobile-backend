from sqlalchemy import Column, Integer, String, BigInteger

from application.core.database import Base
from application.security.models.user import User


class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String)
    full_name = Column(String)
    cpf = Column(String)
    profile_pic = Column(String)
    birthday = Column(BigInteger)
    phone = Column(String)
    hashed_password = Column(String)

    @classmethod
    def from_model(cls, user: User):
        user_db = UserDB(
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.authentication
        )

        return user_db
