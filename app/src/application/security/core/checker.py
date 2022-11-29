from typing import List

from application.core.database import get_db
from application.security.core.helpers import get_current_user
from application.security.models.roles import UserRoles
from application.security.models.user import User
from fastapi import Depends, Header, HTTPException
from requests import Session


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Header(None), db: Session = Depends(get_db)):
        if not token:
            raise HTTPException(status_code=403, detail="Unauthorized")

        user: User = get_current_user(token, db)
        if user.role not in self.allowed_roles:
            print(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


admin_role = RoleChecker([UserRoles.ADMIN.name, UserRoles.INTERNO.value])
