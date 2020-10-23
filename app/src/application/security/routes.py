from datetime import timedelta
from typing import List

from application.shared.base_router import BaseRouter
from sqlalchemy.orm import Session
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from application.security.models.user import User
from application.security.database import repository as security_repository
from application.security.models.token import Token
from application.security.core.helpers import get_password_hash, authenticate_user, create_access_token, \
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from application.core.database import get_db
from application.shared.response import Response, Error


class SecurityRouter(BaseRouter):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")
    security_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.security_router

    @staticmethod
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

    @staticmethod
    @security_router.get("/users/me", response_model=User)
    async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        return get_current_active_user(token, db)

    @staticmethod
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

    @staticmethod
    @security_router.get("/users")
    async def get_all_users(db: Session = Depends(get_db)) -> List[str]:
        return security_repository.get_registered_users(db)

    @staticmethod
    @security_router.post("/users/delete")
    async def delete_user(email: str, db: Session = Depends(get_db)) -> Response:
        user = security_repository.delete_user_by_email(db, email)
        if user:
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="User not found"))
