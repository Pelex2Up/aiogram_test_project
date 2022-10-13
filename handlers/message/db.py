import aiosqlite
from aiogram import types

from loader import dp


@dp.message_handler(commands=['create_db'])
async def create_db(message: types.Message):
    async with aiosqlite.connect('data/data_base/db.sqlite3') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS work_time(day TEXT, open_time TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS booking(full_name TEXT, date TEXT, time TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS menu(dish TEXT, ingredients TEXT, price TEXT)')
        await db.commit()
        await message.answer(text='База данных успешно сформирована')