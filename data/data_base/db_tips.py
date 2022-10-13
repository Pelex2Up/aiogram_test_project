import aiosqlite


async def save_new_dish(dish: str, ingredients: str, price: str):
    async with aiosqlite.connect('db.sqlite3') as db:
        await db.execute('INSERT INTO menu VALUES (?, ?, ?)', (dish, ingredients, price))
        await db.commit()


async def save_new_worktime(day: str, work_time: str):
    async with aiosqlite.connect('db.sqlite3') as db:
        await db.execute('INSERT INTO work_time VALUES (?, ?)', (day, work_time))
        await db.commit()


async def save_booking(name: str, date: str, time: str):
    async with aiosqlite.connect('db.sqlite3') as db:
        await db.execute('INSERT INTO booking VALUES (?, ?, ?)', (name, date, time))
        await db.commit()

