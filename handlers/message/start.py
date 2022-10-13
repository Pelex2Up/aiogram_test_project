from aiogram import types

from keyboards.user.start import start_kb
from loader import dp


@dp.message_handler(commands=['start'])
async def start_user(message: types.Message):
    await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                              f"Тут идет какой-то приветственный текст от маркетологов xD.",
                         reply_markup=await start_kb())

