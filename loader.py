from data.config import BOT_TOKEN, DATA_BASE
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncpg

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

db = await asyncpg.connect(DATA_BASE)
