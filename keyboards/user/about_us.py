from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# async def about_us_kb() -> InlineKeyboardMarkup:
#     keyboard = InlineKeyboardMarkup(
#             row_width=1
#         )
#     keyboard.add(*[
#                 InlineKeyboardButton('Наш номер телефона', callback_data='phone_number'),
#                 InlineKeyboardButton('Время работы', callback_data='work_time'),
#                 InlineKeyboardButton('Адреса кафе', callback_data='adress'),
#                 InlineKeyboardButton('Назад', callback_data='back')
#             ])
#     return keyboard


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
                InlineKeyboardButton(text="Назад", callback_data="back")
            ]
        ]
    )
