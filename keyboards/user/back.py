from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def back_kb(target: str) -> InlineKeyboardMarkup:
    """"
    Клавиатура назад
    :return InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data=target)
            ]
        ]
    )
