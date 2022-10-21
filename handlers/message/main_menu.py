from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.user.start import start_kb
from loader import dp


@dp.callback_query_handler(lambda x: x.data == 'main_menu', state='*')
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text=f"Привет, {callback.from_user.full_name}!\n"
                                          f"Тут идет какой-то приветственный текст от маркетологов xD.",
                                     reply_markup=await start_kb())
