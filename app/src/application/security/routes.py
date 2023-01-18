from datetime import timedelta
from typing import List, Optional

from application.core.database import get_db
from application.security.core.checker import admin_role
from application.security.core.helpers import (ACCESS_TOKEN_EXPIRE_MINUTES,
                                               authenticate_user,
                                               check_password_strength,
                                               check_user_role,
                                               create_access_token,
                                               get_current_active_user,
                                               get_password_hash)
from application.security.database import repository as security_repository
from application.security.models.roles import UserRoles
from application.security.models.token import Token
from application.security.models.user import User
from application.shared.base_router import BaseRouter
from application.shared.response import Error, Response
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status


class SecurityRouter(BaseRouter):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/users/login")
    security_router = APIRouter()

    def __init__(self, prefix: str, app: FastAPI, dependencies: List[Depends] = None):
        super().__init__(prefix, app, dependencies)

    def route(self) -> APIRouter:
        return self.security_router

    
    @staticmethod
    @security_router.get("/users/public")
    async def get_all_users_public(db: Session = Depends(get_db)):
        return security_repository.get_all_users_public(db)

    @staticmethod
    @security_router.post("/users/login", response_model=Token)
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
            data={"email": user.email, "role": user.role}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "role": user.role}

    @staticmethod
    @security_router.get("/users/me", response_model=User)
    async def read_users_me(token: str, db: Session = Depends(get_db)) -> User:
        return get_current_active_user(token, db)

    @staticmethod
    @security_router.post("/users/create")
    async def create_user(user: User, db: Session = Depends(get_db)) -> Response:
        old_user = security_repository.get_user_by_email(db, user.email)
        if old_user:
            return Response(success=False, error=Error(status_code=401, message="Usuário já utilizado."))
        if not check_password_strength(user.authentication, 0.2):
            return Response(success=False, error=Error(status_code=401, message="Senha muito fraca."))
        hashed_password = get_password_hash(user.authentication)
        user.authentication = hashed_password
        saved_user = security_repository.add_user(db, user)
        if saved_user:
            return Response(success=True)
        else:
            raise HTTPException(status_code=403, detail="Not able to create user account")

    @staticmethod
    @security_router.post("/users/create/admin")
    async def create_admin_user(
            user: User, token: Optional[str] = Header(None),
            db: Session = Depends(get_db)
    ) -> Response:
        old_user = security_repository.get_user_by_email(db, user.email)

        if old_user:
            return Response(success=False, error=Error(status_code=401, message="Esse usuário foi utilizado."))
        if not token and security_repository.count_admin_users(db) > 0:
            return Response(success=False, error=Error(status_code=401,
                                                       message="Usuário não tem permissão para criar administradores"))
        if token and security_repository.count_admin_users(db) > 0 and not check_user_role(token, UserRoles.ADMIN, db):
            return Response(success=False, error=Error(status_code=403, message="Não autorizado"))
        if not check_password_strength(user.authentication, 0.3):
            return Response(success=False, error=Error(status_code=401, message="Senha muito fraca."))

        hashed_password = get_password_hash(user.authentication)
        user.authentication = hashed_password
        user.role = UserRoles.ADMIN.name
        saved_user = security_repository.add_user(db, user)
        if saved_user:
            return Response(success=True)
        else:
            raise HTTPException(status_code=403, detail="Não foi possível criar a conta de usuário")

    @staticmethod
    @security_router.get("/users/{user_email}")
    async def get_user_public_by_email(
        user_email: str, db: Session = Depends(get_db)
    ):
        return security_repository.get_user_public_data_by_email(db, user_email)

    @staticmethod
    @security_router.get("/users", dependencies=[Depends(admin_role)])
    async def get_all_users(db: Session = Depends(get_db)) -> List[User]:
        return security_repository.get_registered_users(db)

    @staticmethod
    @security_router.delete("/users/delete", dependencies=[Depends(admin_role)])
    async def delete_user(email: str, db: Session = Depends(get_db)) -> Response:
        user = security_repository.delete_user_by_email(db, email)
        if user:
            return Response(success=True)
        else:
            return Response(success=False, error=Error(status_code=401, message="Usuário não encontrado"))
