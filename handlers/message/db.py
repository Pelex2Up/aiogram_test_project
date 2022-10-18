from aiogram import types
from loader import dp, db


@dp.message_handler(commands=['create_db'])
async def create_db(message: types.Message):
    await message.delete()
    await db.execute("""CREATE TABLE IF NOT EXISTS work_time(day TEXT, open_time TEXT) """)
    await db.execute("""CREATE TABLE IF NOT EXISTS booking(full_name TEXT, date TEXT, time TEXT)""")
    await db.execute("""CREATE TABLE IF NOT EXISTS menu(dish TEXT, ingredients TEXT, price TEXT)""")
    print('База данных успешно сформирована.')
    await db.close()
