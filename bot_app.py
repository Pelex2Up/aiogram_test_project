import datetime
from aiogram.contrib.middlewares.logging import LoggingMiddleware

if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp
    print(f'{datetime.datetime.now()} -- Test_cafe_bot: Начинаю работу.')
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp)
