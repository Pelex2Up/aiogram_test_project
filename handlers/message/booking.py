from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp, bot
from keyboards.user.booking import booking_kb, booking_modify_kb, edit_data_kb
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from keyboards.user.back import back_kb
from states.booking import BookingStates
from aiogram.dispatcher import FSMContext
from datetime import datetime


@dp.callback_query_handler(lambda x: x.data == 'booking')
async def booking(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Бронирование осуществляется за сутки. Максимальное количество человек"
                                                f" за один стол: 6.",
                                           reply_markup=await booking_kb())


@dp.callback_query_handler(lambda x: x.data == 'cancel', state='*')
async def cancel_fsm(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        return
    else:
        await state.finish()
    await callback_query.message.edit_text(text=f"Бронирование осуществляется за сутки. Максимальное количество человек"
                                                f" за один стол: 6.",
                                           reply_markup=await booking_kb())


@dp.callback_query_handler(lambda x: x.data == 'create_booking')
async def start_booking(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id,
                           text='Введите Ваше имя:',
                           reply_markup=await back_kb(target='cancel'))
    await BookingStates.f_name.set()


@dp.message_handler(state=BookingStates.f_name)
async def l_name_booking(message: types.Message, state: FSMContext):
    await state.update_data(f_name=message.text)
    await BookingStates.next()
    await BookingStates.l_name.set()
    await message.delete()
    await message.answer('Введите Вашу фамилию:')


@dp.message_handler(state=BookingStates.l_name)
async def date_booking(message: types.Message, state: FSMContext):
    await state.update_data(l_name=message.text)
    await BookingStates.next()
    await BookingStates.date.set()
    await message.delete()
    await message.answer('Выберите дату:',
                         reply_markup=await SimpleCalendar().start_calendar())


async def is_valid_date(date: str) -> bool:
    today_date = datetime.now().strftime("%d/%m/%Y")
    today_date = today_date.split('/')
    date = date.split('/')
    [d_t, m_t, y_t] = today_date
    [d_ch, m_ch, y_ch] = date
    if d_t <= d_ch and m_t == m_ch and y_t == y_ch:
        return True
    elif m_ch > m_t and y_t <= y_ch:
        return True
    else:
        return False


@dp.callback_query_handler(simple_cal_callback.filter(), state=BookingStates.date)
async def verify_selection(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.edit_text(f'Бронирование на {date.strftime("%d/%m/%Y")}')
        result_select_date = date.strftime("%d/%m/%Y")
        if not await is_valid_date(result_select_date):
            await callback_query.message.answer(f'Выбрана некорректная дата. Проверьте правильность ввода.',
                                                reply_markup=await SimpleCalendar().start_calendar())
        else:
            await state.update_data(date=result_select_date)
            await BookingStates.next()
            await BookingStates.time.set()
            await callback_query.message.edit_text('На какое время хотите забронировать столик?\n'
                                                   'Время вводится в формате Часы:Минуты')


async def is_valid_time(message_time) -> bool:
    message_time = message_time['text'].split(':')
    if 24 > int(message_time[0]) > 00 and 60 >= int(message_time[1]) >= 0:
        return True
    else:
        return False


@dp.message_handler(state=BookingStates.time)
async def booking_time(message: types.Message, state=FSMContext):
    if not await is_valid_time(message):
        await message.delete()
        await message.answer("Время введено не корректно, проверьте правильность ввода.\n"
                             "Формат ввода Часы:Минуты")
    else:

        await state.update_data(time=message.text)
        await BookingStates.next()
        await BookingStates.num_of_people.set()
        await message.delete()
        await message.answer('Время введено корректно и записано.\n'
                             'Введите количество человек')


@dp.message_handler(state=BookingStates.num_of_people)
async def booking_peoples(message: types.Message, state=FSMContext):
    if 0 > int(message.text) > 6:
        await message.delete()
        await message.answer('Количество человек должно быть не больше 6 за один стол.')
    else:
        await state.update_data(num_of_people=message.text)
        booking_data = await state.get_data()
        f_name = booking_data['f_name']
        l_name = booking_data['l_name']
        date = booking_data['date']
        time = booking_data['time']
        number_people = booking_data['num_of_people']
        await message.delete()
        await message.answer(f'Бронь на имя {f_name} {l_name}.\nДата: {date}, время: {time}.\n'
                             f'Количество человек: {number_people}.\n'
                             f'Всё верно?',
                             reply_markup=await booking_modify_kb())


@dp.callback_query_handler(lambda x: x.data == 'commit_booking_data', state=BookingStates.num_of_people)
async def commit_booking(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.edit_text(text='Регистрация прошла успешно',
                                           reply_markup=await back_kb(target='main_menu'))


@dp.callback_query_handler(lambda x: x.data == 'edit_booking_data', state='*')
async def edit_data(callback_query: types.CallbackQuery, state: FSMContext):
    booking_data = await state.get_data()
    f_name = booking_data['f_name']
    l_name = booking_data['l_name']
    date = booking_data['date']
    time = booking_data['time']
    number_people = booking_data['num_of_people']
    await callback_query.message.edit_text(text='Что вы хотите изменить?',
                                           reply_markup=await edit_data_kb(f_name, l_name, date, time, number_people)
                                          )


@dp.callback_query_handler(lambda x: x.data == 'confirm_booking', state='*')
async def confirm_booking(call: types.CallbackQuery, state: FSMContext):
    booking_data = await state.get_data()
    f_name, l_name, date, time, num = booking_data.values()
    await call.message.edit_text(text=f'Бронь на имя {f_name} {l_name}.\nДата: {date}, время: {time}.\n'
                                 f'Количество человек: {num}.\n'
                                 f'Всё верно?',
                                 reply_markup=await booking_modify_kb())