from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link

from keyboards.user.start import start_kb
from loader import dp


# @dp.callback_query_handler(lambda x: x.data == 'main_menu', state='*')
# async def main_menu(callback: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback.message.edit_text(text=f"Привет, {callback.from_user.full_name}!\n"
#                                           f"Тут идет какой-то приветственный текст от маркетологов xD.",
#                                      reply_markup=await start_kb())
@dp.callback_query_handler(lambda x: x.data == 'main_menu', state='*')
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await callback.message.answer_photo(photo='https://www.pngplay.com/wp-content/uploads/7/Cafe-Logo-Background-PNG-Image.png',
                                        caption=f"Привет, {callback.from_user.full_name}!\n"
                                                f"Тут идет какой-то приветственный текст от маркетологов xD.\n",
                                        reply_markup=await start_kb())
