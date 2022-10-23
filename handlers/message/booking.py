from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BadRequest

from crud.users_crud import CRUDUser
from loader import dp, bot
from keyboards.user.booking import booking_kb, booking_modify_kb, edit_data_kb, choice_ppl_kb, \
    edit_choice_ppl_kb, confirm_user_name_kb
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from keyboards.user.back import back_kb
from schemas import UserSchema
from states.booking import BookingStates, BookingEdit
from aiogram.dispatcher import FSMContext
from datetime import datetime
from aiogram_timepicker.panel import FullTimePicker, full_timep_callback


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
    await BookingStates.f_name.set()
    await callback_query.message.edit_text(text=f'Бронирование на имя: '
                                                f'{callback_query.from_user.first_name}?',
                                           reply_markup=await confirm_user_name_kb())


@dp.callback_query_handler(lambda x: x.data == 'use_default_name', state=BookingStates.f_name)
async def f_name_booking(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(f_name=callback_query.from_user.first_name)
    await BookingStates.next()
    await BookingStates.date.set()
    await callback_query.message.edit_text(text=f'{callback_query.from_user.first_name}, выберите дату: ',
                                           reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(lambda x: x.data == 'enter_user_name', state=BookingStates.f_name)
async def fname_select_booking(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text='Введите имя на которое бронируем стол: ')


@dp.message_handler(state=BookingStates.f_name)
async def start_edit_fname_user(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(f_name=message.text)
    await BookingStates.next()
    await BookingStates.date.set()
    for i in range(message.message_id, 0, -1):
        try:
            await bot.edit_message_text(chat_id=message.from_user.id,
                                        message_id=i,
                                        text=f'Бронируем на имя {message.text}.\n'
                                             f'Выберите дату: ',
                                        reply_markup=await SimpleCalendar().start_calendar())
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
                                                   f'На какое время хотите забронировать столик?\n',
                                                   reply_markup=await FullTimePicker().start_picker())


@dp.callback_query_handler(full_timep_callback.filter(), state=BookingStates.time)
async def process_full_timepicker(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    r = await FullTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        result_time = r.time.strftime("%H:%M")
        await state.update_data(time=result_time)
        await BookingStates.next()
        await BookingStates.num_of_people.set()
        await callback_query.message.edit_text(
            f'Вы выбрали {result_time}.\n'
            f'На сколько человек бронируем столик?',
            reply_markup=await choice_ppl_kb()
        )


@dp.callback_query_handler(state=BookingStates.num_of_people)
async def booking_peoples(callback_query: types.CallbackQuery, state=FSMContext):
    no_ppl = int(callback_query.data)
    await state.update_data(num_of_people=no_ppl)
    booking_data = await state.get_data()
    f_name = booking_data['f_name']
    date = booking_data['date']
    time = booking_data['time']
    number_people = booking_data['num_of_people']
    await BookingStates.editing.set()
    await callback_query.message.edit_text(
                text=f'Бронь на имя {f_name}.\nДата: {date}, время: {time}.\n'
                     f'Количество человек: {number_people}.\n'
                     f'Всё верно?',
                reply_markup=await booking_modify_kb())


@dp.callback_query_handler(lambda x: x.data == 'commit_booking_data', state='*')
async def commit_booking(callback_query: types.CallbackQuery, state: FSMContext):
    await BookingStates.editing.set()
    booking_data = await state.get_data()
    confirm_registration = await CRUDUser.add(user=UserSchema(**booking_data))
    if confirm_registration:
        await state.finish()
        await callback_query.message.edit_text(text='Регистрация прошла успешно.\n'
                                                    f'{booking_data["f_name"]}, ваш столик забронирован на '
                                                    f'{booking_data["date"]}, {booking_data["time"]}.',
                                               reply_markup=await back_kb(target='main_menu'))
    else:
        await state.finish()
        await callback_query.message.edit_text(text='Регистрация завершена с ошибкой.\n'
                                                    'Попробуйте снова.',
                                               reply_markup=await back_kb(target='main_menu'))


@dp.callback_query_handler(lambda x: x.data == 'edit_booking_data', state='*')
async def edit_data(callback_query: types.CallbackQuery, state: FSMContext):
    booking_data = await state.get_data()
    f_name = booking_data['f_name']
    date = booking_data['date']
    time = booking_data['time']
    number_people = booking_data['num_of_people']
    await callback_query.message.edit_text(text='Что вы хотите изменить?',
                                           reply_markup=await edit_data_kb(f_name, date, time, number_people))


@dp.callback_query_handler(lambda x: x.data == 'confirm_booking', state='*')
async def confirm_booking(call: types.CallbackQuery, state: FSMContext):
    booking_data = await state.get_data()
    f_name, l_name, date, time, num = booking_data.values()
    await call.message.edit_text(text=f'Бронь на имя {f_name} {l_name}.\nДата: {date}, время: {time}.\n'
                                      f'Количество человек: {num}.\n'
                                      f'Всё верно?',
                                 reply_markup=await booking_modify_kb())


@dp.callback_query_handler(lambda x: x.data == 'edit_fname', state='*')
async def edit_fname_handler(call: types.CallbackQuery, state: FSMContext):
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


@dp.callback_query_handler(lambda x: x.data == 'edit_time', state='*')
async def edit_time_handler(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.time_edit.set()
    await call.message.edit_text(text=f'На какое время хотите забронировать столик?\n',
                                 reply_markup=await FullTimePicker().start_picker())


@dp.callback_query_handler(full_timep_callback.filter(), state=BookingEdit.time_edit)
async def edit_time(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await BookingStates.time.set()
    r = await FullTimePicker().process_selection(callback_query, callback_data)
    if r.selected:
        result_time = r.time.strftime("%H:%M")
        await state.update_data(time=result_time)
        await BookingStates.next()
        await BookingEdit.next()
        await BookingStates.editing.set()
        await BookingEdit.editing.set()
        await callback_query.message.edit_text(text=f'Время успешно изменена на: {result_time}',
                                               reply_markup=await back_kb(target='edit_booking_data',
                                                                          text='OK'))


@dp.callback_query_handler(lambda x: x.data == 'edit_ppl', state='*')
async def edit_ppl_handler(call: types.CallbackQuery, state: FSMContext):
    await BookingEdit.ppl_edit.set()
    await call.message.edit_text(text='Выберите количество человек:',
                                 reply_markup=await edit_choice_ppl_kb(target='edit_booking_data'))


@dp.callback_query_handler(state=BookingEdit.ppl_edit)
async def edit_ppl(callback_query: types.CallbackQuery, state: FSMContext):
    await BookingStates.num_of_people.set()
    await state.update_data(num_of_people=callback_query.data)
    await BookingStates.next()
    await BookingEdit.next()
    await BookingStates.editing.set()
    await BookingEdit.editing.set()
    await callback_query.message.edit_text(text=f'Количество человек успешно изменено на: {callback_query.data}',
                                           reply_markup=await back_kb(target='edit_booking_data',
                                                                      text='OK'))


@dp.callback_query_handler(lambda x: x.data == 'edit_date', state='*')
async def edit_date_handler(call: types.CallbackQuery, state: FSMContext):
    await BookingStates.editing.set()
    await BookingEdit.date_edit.set()
    await call.message.edit_text(text='Выберите дату: ',
                                 reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=BookingEdit.date_edit)
async def edit_date(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(query=call, data=callback_data)
    if selected:
        result_select_date = date.strftime("%d/%m/%Y")
        if not await is_valid_date(result_select_date):
            await call.message.edit_text(f'Выбрана некорректная дата {date.strftime("%d/%m/%Y")}\n'
                                         f'Проверьте правильность ввода.',
                                         reply_markup=await SimpleCalendar().start_calendar())
        else:
            await BookingStates.date.set()
            await state.update_data(date=result_select_date)
            await BookingStates.next()
            await BookingEdit.next()
            await BookingStates.editing.set()
            await BookingEdit.editing.set()
            await call.message.edit_text(text=f'Дата успешно изменена на: {date.strftime("%d/%m/%Y")}',
                                         reply_markup=await back_kb(target='edit_booking_data',
                                                                    text='OK'))