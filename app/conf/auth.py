
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from starlette.exceptions import HTTPException

from app.conf.hashing import verify_password
from app.db.session import get_session
from app.models.user import User
from app.conf.settings import settings


class TokenData(BaseModel):
    name: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


async def authenticate(
    *,
    email: str,
    password: str,
    session: AsyncSession,
) -> Optional[User]:
    user = await User.get_by_email(session, email)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with email {email} not found")
    is_verified = await verify_password(password, user.password_hash)
    if is_verified:
        return user


async def create_access_token(*, sub: str) -> str:
    return await _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


async def _create_token(token_type: str, lifetime: timedelta, sub: str,) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except JWTError:
        raise credentials_exception
    user = (await session.execute(select(User).where(User.name == token_data.name))).first()
    if user is None:
        raise credentials_exception
    return user.User
