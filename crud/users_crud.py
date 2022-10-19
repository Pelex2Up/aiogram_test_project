from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserSchema, UserInDBSchema
from models import UsersBooking, create_async_session


class CRUDUser(object):

    @staticmethod
    @create_async_session
    async def add(user: UserSchema, session: AsyncSession = None) -> UserInDBSchema | None:
        user = UsersBooking(**user.dict())
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(user)
            return UserInDBSchema(**user.__dict__)

    @staticmethod
    @create_async_session
    async def delete(user_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(UsersBooking)
            .where(UsersBooking.id == user_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(user_id: int, session: AsyncSession = None) -> UserInDBSchema | None:
        user = await session.execute(
            select(UsersBooking)
            .where(UsersBooking.id == user_id)
        )
        if user := user.first():
            return UserInDBSchema(**user[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[UserInDBSchema]:
        users = await session.execute(
            select(UsersBooking)
        )
        return [UserInDBSchema(**user[0].__dict__) for user in users]
