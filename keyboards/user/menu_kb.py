from aiogram.types import InlineKeyboardButton as button, InlineKeyboardMarkup, ParseMode


async def menu_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для отображения и перелистывания меню кафе.
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                button(text='⭠', callback_data='roll_back'),
                button(text='⭢', callback_data='roll_forward'),
                button(text='≣', callback_data='options')
            ],
            [
                button(text='В главное меню', callback_data='main_menu')
            ]
        ]
    )