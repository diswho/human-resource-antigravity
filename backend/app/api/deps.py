from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import get_session
from app.models.user import TokenPayload, User, UserRole

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges (Admin required)"
        )
    return current_user

def get_current_active_hr(current_user: CurrentUser) -> User:
    if current_user.role not in [UserRole.admin, UserRole.hr]:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges (HR or Admin required)"
        )
    return current_user

# Keep for backward compatibility if needed, but point to Admin check
def get_current_active_superuser(current_user: CurrentUser) -> User:
    return get_current_active_admin(current_user)
