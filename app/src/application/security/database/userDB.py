from application.core.database import Base
from application.security.models.user import User
from sqlalchemy import BigInteger, Column, Integer, String, UniqueConstraint, Boolean


class UserDB(Base):
    __tablename__ = "user"

    # id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    cpf = Column(String)
    picture = Column(String)
    birthday = Column(BigInteger)
    phone = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    anonymous = Column(Boolean, default=False)

    @classmethod
    def from_model(cls, user: User):
        user_db = UserDB(
            email=user.email,
            full_name=user.full_name,
            picture=user.picture,
            hashed_password=user.authentication,
            role = user.role,
            anonymous = user.anonymous
        )

        return user_db
