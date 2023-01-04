from application.security.models.roles import UserRoles
from fastapi import HTTPException
from passlib.context import CryptContext
from password_strength import PasswordStats
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError

from application.security.database import repository as security_repository
from application.core import config

from starlette import status

from application.security.models.user import User

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = security_repository.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def check_user_role(token: str, role: UserRoles, db: Session) -> bool:
    current_user: User = get_current_user(token, db)
    return current_user.role == role.name


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str, db: Session) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = security_repository.get_user_by_email(db, email=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(token: str, db: Session) -> User:
    current_user: User = get_current_user(token, db)
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(email=current_user.email, full_name=current_user.full_name, picture=current_user.picture, authentication=token)


def check_password_strength(password: str, minimum: float) -> bool:
    stats = PasswordStats(password)
    return stats.strength() >= minimum
