from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from loader import dp, bot
from keyboards.user.booking import booking_kb, booking_modify_kb, edit_data_kb, confirm_edit_kb
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from keyboards.user.back import back_kb
from states.booking import BookingStates, BookingEdit
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

    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=i,
                text='Введите Вашу фамилию:'
            )
        except BadRequest:
            pass


@dp.message_handler(state=BookingStates.l_name)
async def date_booking(message: types.Message, state: FSMContext):
    await state.update_data(l_name=message.text)
    await BookingStates.next()
    await BookingStates.date.set()
    await message.delete()

    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=i,
                text='Выберите дату: ',
                reply_markup=await SimpleCalendar().start_calendar()
            )
        except BadRequest:
            pass


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
        result_select_date = date.strftime("%d/%m/%Y")
        if not await is_valid_date(result_select_date):
            await callback_query.message.edit_text(f'Выбрана некорректная дата {date.strftime("%d/%m/%Y")}\n'
                                                   f'Проверьте правильность ввода.',
                                                   reply_markup=await SimpleCalendar().start_calendar())
        else:
            await state.update_data(date=result_select_date)
            await BookingStates.next()
            await BookingStates.time.set()
            await callback_query.message.edit_text(f'Дата бронирования: {date.strftime("%d/%m/%Y")}.\n'
                                                   f'На какое время хотите забронировать столик?\n'
                                                   f'Время вводится в формате Часы:Минуты')


async def is_valid_time(message_time) -> bool:
    message_time = message_time['text'].split(':')
    if len(message_time[0]) == 2 and len(message_time[1]) == 2:
        if 24 > int(message_time[0]) >= 00 and 60 >= int(message_time[1]) >= 0:
            return True
        else:
            return False
    else:
        return False


@dp.message_handler(state=BookingStates.time)
async def booking_time(message: types.Message, state=FSMContext):
    if not await is_valid_time(message):
        await message.delete()
        await message.answer(text="Время введено не корректно, проверьте правильность ввода.\n"
                                  "Формат ввода Часы:Минуты")
    else:
        await state.update_data(time=message.text)
        await BookingStates.next()
        await BookingStates.num_of_people.set()
        await message.delete()

    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=i,
                text='Время введено корректно и записано.\n'
                     'Введите количество человек (от 1 до 6):'
            )
        except BadRequest:
            pass


@dp.message_handler(state=BookingStates.num_of_people)
async def booking_peoples(message: types.Message, state=FSMContext):
    if 0 > int(message.text) > 6:
        await message.delete()
        await message.answer(text='Количество человек должно быть не больше 6 за один стол.')
    else:
        await state.update_data(num_of_people=message.text)
        booking_data = await state.get_data()
        f_name = booking_data['f_name']
        l_name = booking_data['l_name']
        date = booking_data['date']
        time = booking_data['time']
        number_people = booking_data['num_of_people']
        await message.delete()

        for i in range(message.message_id, 0, -1):
            try:
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=i,
                    text=f'Бронь на имя {f_name} {l_name}.\nДата: {date}, время: {time}.\n'
                         f'Количество человек: {number_people}.\n'
                         f'Всё верно?',
                    reply_markup=await booking_modify_kb()
                )
            except BadRequest:
                pass


@dp.callback_query_handler(lambda x: x.data == 'commit_booking_data', state='*')
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
                                           reply_markup=await edit_data_kb(f_name, l_name, date, time, number_people))


@dp.callback_query_handler(lambda x: x.data == 'confirm_booking', state='*')
async def confirm_booking(call: types.CallbackQuery, state: FSMContext):
    booking_data = await state.get_data()
    f_name, l_name, date, time, num = booking_data.values()
    await call.message.edit_text(text=f'Бронь на имя {f_name} {l_name}.\nДата: {date}, время: {time}.\n'
                                      f'Количество человек: {num}.\n'
                                      f'Всё верно?',
                                 reply_markup=await booking_modify_kb())


@dp.callback_query_handler(lambda x: x.data == 'edit_fname', state='*')
async def edit_fname(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.fname_edit.set()
    await call.message.edit_text(text='Введите измененное имя:',
                                 reply_markup=await back_kb(target='edit_booking_data'))


@dp.message_handler(state=BookingEdit.fname_edit)
async def edit_fname(message: types.Message, state: FSMContext):
    await BookingStates.f_name.set()
    await state.update_data(f_name=message.text)
    await message.delete()
    await BookingStates.next()
    await BookingEdit.next()
    await BookingStates.editing.set()
    await BookingEdit.editing.set()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(chat_id=message.from_user.id,
                                        message_id=i,
                                        text=f'Имя успешно изменено на: {message.text}',
                                        reply_markup=await back_kb(target='edit_booking_data',
                                                                   text='OK'))
        except BadRequest:
            pass


@dp.callback_query_handler(lambda x: x.data == 'edit_lname', state='*')
async def edit_fname(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.lname_edit.set()
    await call.message.edit_text(text='Введите измененную фамилию:',
                                 reply_markup=await back_kb(target='edit_booking_data'))


@dp.message_handler(state=BookingEdit.lname_edit)
async def edit_fname(message: types.Message, state: FSMContext):
    await BookingStates.l_name.set()
    await state.update_data(l_name=message.text)
    await message.delete()
    await BookingStates.next()
    await BookingEdit.next()
    await BookingStates.editing.set()
    await BookingEdit.editing.set()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(chat_id=message.from_user.id,
                                        message_id=i,
                                        text=f'Фамилия успешно изменена на: {message.text}',
                                        reply_markup=await back_kb(target='edit_booking_data',
                                                                   text='OK'))
        except BadRequest:
            pass


@dp.callback_query_handler(lambda x: x.data == 'edit_time', state='*')
async def edit_fname(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.time_edit.set()
    await call.message.edit_text(text='Введите новое время:',
                                 reply_markup=await back_kb(target='edit_booking_data'))


@dp.message_handler(state=BookingEdit.time_edit)
async def edit_fname(message: types.Message, state: FSMContext):
    await BookingStates.time.set()
    await state.update_data(time=message.text)
    await message.delete()
    await BookingStates.next()
    await BookingEdit.next()
    await BookingStates.editing.set()
    await BookingEdit.editing.set()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(chat_id=message.from_user.id,
                                        message_id=i,
                                        text=f'Время успешно изменена на: {message.text}',
                                        reply_markup=await back_kb(target='edit_booking_data',
                                                                   text='OK'))
        except BadRequest:
            pass


@dp.callback_query_handler(lambda x: x.data == 'edit_ppl', state='*')
async def edit_fname(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.ppl_edit.set()
    await call.message.edit_text(text='Введите количество человек:',
                                 reply_markup=await back_kb(target='edit_booking_data'))


@dp.message_handler(state=BookingEdit.ppl_edit)
async def edit_fname(message: types.Message, state: FSMContext):
    await BookingStates.num_of_people.set()
    await state.update_data(num_of_people=message.text)
    await message.delete()
    await BookingStates.next()
    await BookingEdit.next()
    await BookingStates.editing.set()
    await BookingEdit.editing.set()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(chat_id=message.from_user.id,
                                        message_id=i,
                                        text=f'Количество человек успешно изменено на: {message.text}',
                                        reply_markup=await back_kb(target='edit_booking_data',
                                                                   text='OK'))
        except BadRequest:
            pass