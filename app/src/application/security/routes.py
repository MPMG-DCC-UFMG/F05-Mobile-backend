from datetime import timedelta

from sqlalchemy.orm import Session
from starlette import status

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from application.security.models.user import User
from application.security.database import repository as security_repository
from application.security.models.token import Token, TokenData
from application.security.core.helpers import get_password_hash, verify_password, authenticate_user, \
    create_access_token, get_current_user, get_current_active_user
from application.core.database import get_db
from application.shared.response import Response, Error

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")
security_router = APIRouter()


@security_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@security_router.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    return get_current_active_user(token, db)


@security_router.post("/users/create")
async def create_user(user: User, db: Session = Depends(get_db)) -> Response:
    old_user = security_repository.get_user_by_email(db, user.email)
    if old_user:
        return Response(success=False, error=Error(status_code=401, message="Email already exist in database"))

    hashed_password = get_password_hash(user.authentication)
    user.authentication = hashed_password
    saved_user = security_repository.add_user(db, user)
    if saved_user:
        return Response(success=True)
    else:
        raise HTTPException(status_code=403, detail="Not able to create user account")
