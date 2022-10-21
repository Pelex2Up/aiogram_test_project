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


async def edit_data_kb(f_name, l_name, date, time, num_of_people) -> InlineKeyboardMarkup:
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
                InlineKeyboardButton(text=f'Фамилия -> {l_name}', callback_data='edit_lname')
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
