from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf.auth import (
    authenticate,
    create_access_token
)
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import CreateUserRequest, CreateUserResponse

router = APIRouter()


@router.post("/login")
async def login(
        session: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = await authenticate(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = await create_access_token(sub=user.email)
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/signup", status_code=201, response_model=CreateUserResponse)
async def create_user_signup(
        *,
        session: AsyncSession = Depends(get_session),
        payload: CreateUserRequest,
) -> CreateUserResponse | None:
    """
    Create new user without the need to be logged in.
    """
    
    user = await User.get_by_email(session, payload.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = await User.create(session, payload)
    return user
