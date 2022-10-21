from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import hide_link

from crud.menu_crud import CRUDMenu
from loader import dp, bot
from keyboards.user.menu_kb import menu_kb


@dp.callback_query_handler(lambda x: x.data == 'menu')
async def food_menu(callback_query: types.CallbackQuery, food_id: int = 1):
    get_food = await CRUDMenu.get(food_id=food_id)
    if get_food:
        await callback_query.message.edit_text(text=f"sfsajkf\n"
                                                    f'asfkasfjsa',
                                               reply_markup=await menu_kb(),
                                               parse_mode=ParseMode.HTML)


# @dp.callback_query_handler(lambda x: x.data == '')