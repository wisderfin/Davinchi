from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.base.database import get_async_session
from app.model import UserModel


async def get_user(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            return user
        return None


async def create_user(data: dict):
    async for session in get_async_session():
        user = UserModel(**data)
        session.add(user)
        await session.commit()

