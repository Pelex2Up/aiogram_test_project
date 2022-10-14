from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def booking_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для бронирования столика
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Забронировать столик', callback_data='create_booking')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='main_menu')
            ]
        ]
    )