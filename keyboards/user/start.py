from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_kb() -> InlineKeyboardMarkup:
    """
    Стартовая клавиатура
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Меню', callback_data='menu')
            ],
            [
                InlineKeyboardButton('О ресторане', callback_data='about_us')
            ],
            [
                InlineKeyboardButton('Бронирование столика', callback_data='booking')
            ]
        ]
    )
