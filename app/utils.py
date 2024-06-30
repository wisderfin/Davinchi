from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.base.database import get_async_session
from app.model import UserModel
from app.service import long_by_coordinate


async def get_user(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            return user
        return None


async def get_users(location: str, age: int, gender: bool, lat: float, lon: float):
    async for session in get_async_session():
        min_age = age - 7
        max_age = age + 7

        # Получаем пользователей по базе данных с заданными условиями
        query = select(UserModel).filter(
            and_(
                UserModel.location == location,
                UserModel.gender == gender,
                UserModel.age >= min_age,
                UserModel.age <= max_age
            )
        )
        result = await session.execute(query)
        users = result.scalars().all()

        # Фильтруем пользователей по расстоянию на уровне Python
        filtered_users = [
            user for user in users
            if long_by_coordinate(user.lat, user.lon, lat, lon) <= 70
        ]

        return filtered_users if filtered_users is not None else None


async def create_user(data: dict):
    async for session in get_async_session():
        user = UserModel(**data)
        session.add(user)
        await session.commit()


async def edit_name(id: int, new_name: str):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.name = new_name
            await session.commit()


async def edit_age(id: int, new_age: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.age = new_age
            await session.commit()


async def edit_gender(id: int, new_gender: bool):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.gender = new_gender
            await session.commit()


async def edit_location(id: int, new_location: str):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.location = new_location
            await session.commit()


async def edit_photo(id: int, new_photo: str):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.photos = new_photo
            await session.commit()


async def edit_description(id: int, new_description: str):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.description = new_description
            await session.commit()


async def user_banned(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.banned = True
            await session.commit()


async def user_unbanned(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.banned = False
            await session.commit()


async def set_admin(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.admin = True
            await session.commit()


async def unset_admin(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.admin = False
            await session.commit()


async def check_banned(id: int):
    async for session in get_async_session():
        result = await session.execute(select(UserModel).filter_by(id=id))
        user = result.scalar_one_or_none()
        return user.banned
