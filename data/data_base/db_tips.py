import asyncpg
from data.config import DATA_BASE


async def booking_update_db(fname, date, time):
    con = await asyncpg.connect(DATA_BASE)
    await con.execute('INSERT INTO booking(full_name, date, time) VALUES (%s, %s, %s)', (fname, date, time))
    await con.close()

