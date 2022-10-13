from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    keyboard.add(*[
        InlineKeyboardButton('Меню', callback_data='menu'),
        InlineKeyboardButton('О ресторане', callback_data='about_us'),
        InlineKeyboardButton('Бронирование столика', callback_data='booking')
    ])
    return keyboard
