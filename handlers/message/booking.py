from aiogram import types

from loader import dp
from keyboards.user.back import back_kb


@dp.callback_query_handler(lambda x: x.data == 'booking')
async def about_us(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Заглушка",
                                           reply_markup=await back_kb())