from __future__ import annotations

import enum
from typing import Optional

from sqlalchemy import Integer, String, Column, Enum, Text, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf.hashing import get_password_hash
from app.db.base_class import Base


class RoleEnum(str, enum.Enum):
    SIMPLE = "simple"
    ADVANCED = "advanced"
    ADMIN = "admin"


class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256), index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password_hash = Column(Text, nullable=False)
    
    @classmethod
    async def get_by_email(cls, session: AsyncSession, user_email: str) -> Optional[User]:
        query = select(cls).where(cls.email == user_email)
        result = (await session.execute(query)).first()
        return result.User if result else None
    
    @classmethod
    async def create(cls, session: AsyncSession, user) -> Optional[User]:
        user_dict = user.dict()
        user_dict.pop("password")
        new_user = User(**user_dict)
        new_user.password_hash = await get_password_hash(user.password)
        
        session.add(new_user)
        await session.commit()
        user = await cls.get_by_email(session, new_user.email)
        if not user:
            raise RuntimeError()
        return user
