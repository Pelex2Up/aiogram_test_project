from aiogram import types

from loader import dp
from keyboards.user.start import start_kb


@dp.callback_query_handler(lambda x: x.data == 'back')
async def back_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f'Рады видеть вас, {callback_query.from_user.first_name}! '
                                                f'Добро пожаловать в наше кафе!\n'
                                                f'Выберите то, что вас интересует.',
                                           reply_markup=await start_kb())
