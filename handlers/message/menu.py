from aiogram import types

from loader import dp, bot
from keyboards.user.back import back_kb


@dp.callback_query_handler(lambda x: x.data == 'menu')
async def about_us(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Сегодня в меню ничего нет, но "
                                                f"вы потыкайте разработчика, мб появится :)\n"
                                                f"База данных с блюдами еще не заполнена.",
                                           reply_markup=await back_kb(target="main_menu"))
