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


async def booking_modify_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для подтверждения данных или редактирования при бронировании столика
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data='commit_booking_data')
            ],
            [
                InlineKeyboardButton(text='Нет, нужно исправить', callback_data='edit_booking_data')
            ]
        ]
    )


async def edit_data_kb(f_name, date, time, num_of_people) -> InlineKeyboardMarkup:
    """
    Клавиатура редактирования данных пользователя
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Имя -> {f_name}', callback_data='edit_fname')
            ],
            [
                InlineKeyboardButton(text=f'Дата -> {date}', callback_data='edit_date')
            ],
            [
                InlineKeyboardButton(text=f'Время -> {time}', callback_data='edit_time')
            ],
            [
                InlineKeyboardButton(text=f'Количество человек -> {num_of_people}', callback_data='edit_ppl')
            ],
            [
                InlineKeyboardButton(text=f'Назад', callback_data='confirm_booking')
            ]
        ]
    )


async def confirm_edit_kb(edit: str, back: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Подтвердить', callback_data=edit),
                InlineKeyboardButton(text='Назад', callback_data=back)
            ]
        ]
    )


async def choice_ppl_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3')
            ],
            [
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6')
            ]
        ]
    )


async def edit_choice_ppl_kb(target: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3')
            ],
            [
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=target)
            ]
        ]
    )


async def confirm_user_name_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Нет', callback_data='enter_user_name'),
                InlineKeyboardButton(text='Да', callback_data='use_default_name')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='cancel')
            ]
        ]
    )