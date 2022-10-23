import datetime
import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils.set_bot_commands import set_default_commands
from aiogram_timepicker.panel import full_timep_default


async def on_startup(dp):
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp

    # print(f'{datetime.datetime.now()} -- Test_cafe_bot: Начинаю работу.')
    logging.basicConfig(level=logging.INFO)
    # dp.middleware.setup(LoggingMiddleware())
    full_timep_default(
        # default labels
        label_up='↑', label_down='↓',
        hour_format='{0:02}ч', minute_format='{0:02}м'
    )
    executor.start_polling(dp, on_startup=on_startup)
