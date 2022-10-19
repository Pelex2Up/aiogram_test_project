# import asyncpg
# from data.config import DATA_BASE
# from loader import db
#
#
# async def booking_update_db(fname, date, time):
#     await db.execute('INSERT INTO booking(full_name, date, time) VALUES (%s, %s, %s)', (fname, date, time))
#     await db.close()
#
