from sqlalchemy.orm import Session

from application.security.models.user import User
from application.security.database.userDB import UserDB


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(UserDB).filter(UserDB.email == email).first()


def add_user(db: Session, user: User) -> User:
    db_user = UserDB.from_model(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
