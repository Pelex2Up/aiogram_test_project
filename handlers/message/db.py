import aiosqlite
from aiogram import types
import asyncpg
from data.config import DATA_BASE

from loader import dp


@dp.message_handler(commands=['create_db'])
async def create_db(message: types.Message):
    await message.delete()
    con = await asyncpg.connect(DATA_BASE)
    print('База данных успешно открыта.')
    await con.execute("""CREATE TABLE IF NOT EXISTS work_time(day TEXT, open_time TEXT) """)
    await con.execute("""CREATE TABLE IF NOT EXISTS booking(full_name TEXT, date TEXT, time TEXT)""")
    await con.execute("""CREATE TABLE IF NOT EXISTS menu(dish TEXT, ingredients TEXT, price TEXT)""")
    print('База данных успешно сформирована.')
    await con.close()
