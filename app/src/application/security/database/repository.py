from typing import List

from application.security.database.userDB import UserDB
from application.security.models.roles import UserRoles
from application.security.models.user import User
from sqlalchemy.orm import Session, load_only


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(UserDB).filter(UserDB.email == email).first()


def get_user_public_data_by_email(db: Session, user_email: str) -> list:
    columns = ["email", "full_name", "picture", "role", "expo_token", "anonymous"]
    user_db = db.query(UserDB).options(load_only(*columns)).get(user_email)
    if user_db:
        return user_db


def get_all_users_public(db: Session) -> list:
    columns = ["email", "full_name", "picture", "role", "anonymous", "expo_token"]
    users_db = db.query(UserDB).options(load_only(*columns)).all()

    return users_db


def delete_user_by_email(db: Session, email: str) -> User:
    db_user = db.query(UserDB).filter(UserDB.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def add_user(db: Session, user: User) -> User:
    db_user = UserDB.from_model(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_registered_users(db: Session) -> List[User]:
    db_users = db.query(UserDB).all()
    return db_users


def count_users(db: Session) -> int:
    db_users = db.query(UserDB).all()
    return db_users.count()


def count_admin_users(db: Session) -> int:
    db_users = db.query(UserDB).filter(UserDB.role == UserRoles.ADMIN.name)
    return db_users.count()
