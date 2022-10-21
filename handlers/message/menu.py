from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.markdown import hide_link

from crud.menu_crud import CRUDMenu
from keyboards import back_kb
from loader import dp, bot
from keyboards.user.menu_kb import menu_kb
from states import MenuStates


@dp.callback_query_handler(lambda x: x.data == 'menu')
async def start_food_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await MenuStates.id.set()
    await state.update_data(id=1)
    food_id = await state.get_data()
    get_food = await CRUDMenu.get(food_id=food_id['id'])
    food_photo = get_food.food_photo
    name = get_food.food_name
    price = get_food.food_price
    if get_food:
        await callback_query.message.edit_text(text=f"{hide_link(food_photo)}\n"
                                                    f'<b>{name}</b>\n\n{price}',
                                               reply_markup=await menu_kb(),
                                               parse_mode=ParseMode.HTML)


@dp.callback_query_handler(lambda x: x.data == 'options', state=MenuStates)
async def food_comp(callback_query: types.CallbackQuery, state: FSMContext):
    food_id = await state.get_data()
    get_comp = await CRUDMenu.get(food_id=food_id['id'])
    if get_comp:
        food_compound = get_comp.food_compound
        await callback_query.message.edit_text(text=f'{food_compound}',
                                               reply_markup=await back_kb(target='menu_options'))


@dp.callback_query_handler(lambda x: x.data == 'menu_options', state=MenuStates)
async def food_menu(callback_query: types.CallbackQuery, state: FSMContext):
    food_id = await state.get_data()
    get_food = await CRUDMenu.get(food_id=food_id['id'])
    food_photo = get_food.food_photo
    name = get_food.food_name
    price = get_food.food_price
    if get_food:
        await callback_query.message.edit_text(text=f"{hide_link(food_photo)}\n"
                                                    f'<b>{name}</b>\n\n{price}',
                                               reply_markup=await menu_kb(),
                                               parse_mode=ParseMode.HTML)


@dp.callback_query_handler(lambda x: x.data == 'roll_forward', state=MenuStates)
async def next_food_menu(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(id=data['id']+1)
    food_id = await state.get_data()
    get_food = await CRUDMenu.get(food_id=food_id['id'])
    food_photo = get_food.food_photo
    name = get_food.food_name
    price = get_food.food_price
    if get_food:
        await callback_query.message.edit_text(text=f"{hide_link(food_photo)}\n"
                                                    f'<b>{name}</b>\n\n{price}',
                                               reply_markup=await menu_kb(),
                                               parse_mode=ParseMode.HTML)


@dp.callback_query_handler(lambda x: x.data == 'roll_back', state=MenuStates)
async def back_food_menu(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(id=data['id']-1)
    food_id = await state.get_data()
    get_food = await CRUDMenu.get(food_id=food_id['id'])
    food_photo = get_food.food_photo
    name = get_food.food_name
    price = get_food.food_price
    if get_food:
        await callback_query.message.edit_text(text=f"{hide_link(food_photo)}\n"
                                                    f'<b>{name}</b>\n\n{price}',
                                               reply_markup=await menu_kb(),
                                               parse_mode=ParseMode.HTML)

