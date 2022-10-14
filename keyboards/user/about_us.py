from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def about_us_kb() -> InlineKeyboardMarkup:
    """"
    Описание что делает функция
    :param Какие параметры принимает и для чего
    :return Что будет на выходе
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Наш номер телефона", callback_data="phone_number")
            ],
            [
                InlineKeyboardButton(text="Время работы", callback_data="work_time")
            ],
            [
                InlineKeyboardButton(text="Адреса кафе", callback_data="adress")
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data="main_menu")
            ]
        ]
    )
