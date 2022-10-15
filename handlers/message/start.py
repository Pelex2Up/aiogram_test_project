from aiogram import types

from keyboards.user.start import start_kb
from loader import dp, bot


@dp.message_handler(commands=['start'])
async def start_user(message: types.Message):
    await message.delete()
    try:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=f"Привет, {message.from_user.full_name}!\n"
                                         f"Тут идет какой-то приветственный текст от маркетологов xD.",
                                    reply_markup=await start_kb())
    except Exception as ex:
        await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                                  f"Тут идет какой-то приветственный текст от маркетологов xD.",
                             reply_markup=await start_kb())
