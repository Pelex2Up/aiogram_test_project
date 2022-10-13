from aiogram import types

from loader import dp, bot
from keyboards.user.back import back_kb


@dp.callback_query_handler(lambda x: x.data == 'work_time')
async def about_us(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Режим работы будет подсасываться из базы данных :)",
                                           reply_markup=await back_kb())
