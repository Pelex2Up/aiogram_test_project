from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def back_kb(target: str, text='Назад') -> InlineKeyboardMarkup:
    """"
    Клавиатура назад
    :return InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=target)
            ]
        ]
    )
