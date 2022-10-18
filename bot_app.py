import datetime

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp

    print(f'{datetime.datetime.now()} -- Test_cafe_bot: Начинаю работу.')
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp , on_startup=on_startup)
