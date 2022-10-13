from data import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
