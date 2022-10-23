from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from inline_timepicker.inline_timepicker import InlineTimepicker

from config import CONFIG

bot = Bot(
    token=CONFIG.BOT.TOKEN,
    parse_mode=ParseMode.HTML
)
storage = MemoryStorage()
dp = Dispatcher(
    bot=bot,
    storage=storage
)