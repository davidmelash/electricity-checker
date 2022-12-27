from typing import Sequence

from pydantic import BaseModel, EmailStr

from app.models.user import RoleEnum


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum


class UserSchemaBase(UserBase):
    class Config:
        use_enum_values = True
        orm_mode = True


class CreateUserResponse(UserSchemaBase):
    ...


class UpdateUserResponse(UserSchemaBase):
    ...


class GetUserResponse(UserSchemaBase):
    ...


class GetAllUsersResponse(UserSchemaBase):
    results: Sequence[UserSchemaBase]


class UpdateUserRequest(UserBase):
    ...


class CreateUserRequest(UserBase):
    password: str
