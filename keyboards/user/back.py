from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def back_kb(target: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
            row_width=1
        )
    keyboard.add(*[
                InlineKeyboardButton('Назад', callback_data=target)
            ])
    return keyboard
