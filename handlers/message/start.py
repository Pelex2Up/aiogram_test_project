from aiogram import types

from keyboards.user.start import start_kb
from loader import dp, bot


@dp.message_handler(commands=['start'])
async def start_user(message: types.Message):
    await message.delete()
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://www.pngplay.com/wp-content/uploads/7/Cafe-Logo-Background-PNG-Image.png',
                         caption=f"Привет, {message.from_user.full_name}!\n"
                                 f"Тут идет какой-то приветственный текст от маркетологов xD.\n",
                         reply_markup=await start_kb())
