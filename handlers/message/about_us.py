from aiogram import types

from keyboards.user.about_us import about_us_kb
from keyboards.user.back import back_kb

from loader import dp


@dp.callback_query_handler(lambda x: x.data == 'about_us')
async def about_us(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(text=f"Что вы хотели бы узнать про нас?",
                                        reply_markup=await about_us_kb())


@dp.callback_query_handler(lambda x: x.data == 'phone_number')
async def about_us_phone(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Наш номер телефона: +121983258923",
                                           reply_markup=await back_kb(target='about_us'))


@dp.callback_query_handler(lambda x: x.data == 'adress')
async def about_us_adress(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Наши адреса: \nг. Минск, ул. Хзкакаятоулица, д.12\n"
                                                f"г.Минск, ул. Тожехзкакаяулица, д.125",
                                           reply_markup=await back_kb(target='about_us'))


@dp.callback_query_handler(lambda x: x.data == 'work_time')
async def about_us_work_time(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=f"Режим работы кафе пока в разработке. База данных не заполнена.",
                                           reply_markup=await back_kb(target='about_us'))


@dp.callback_query_handler(lambda x: x.data == 'test_button')
async def test_data_func(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f'{callback_query.data}')