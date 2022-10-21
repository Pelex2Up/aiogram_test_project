from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import MenuChoice, create_async_session
from schemas import MenuSchema, MenuInDBSchema


class CRUDMenu(object):

    @staticmethod
    @create_async_session
    async def add(menu: MenuSchema, session: AsyncSession = None) -> MenuInDBSchema | None:
        menu = MenuChoice(**menu.dict())
        session.add(menu)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(menu)
            return MenuInDBSchema(**menu.__dict__)

    @staticmethod
    @create_async_session
    async def get(food_id: int, session: AsyncSession = None) -> MenuInDBSchema | None:
        food = await session.execute(select(MenuChoice)
                                     .where(MenuChoice.id == food_id)
                                     )
        if food := food.first():
            return MenuInDBSchema(**food[0].__dict__)
