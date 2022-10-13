from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def back_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
            row_width=1
        )
    keyboard.add(*[
                InlineKeyboardButton('Назад', callback_data='back')
            ])
    return keyboard
