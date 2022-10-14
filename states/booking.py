from aiogram.dispatcher.filters.state import State, StatesGroup


class BookingStates(StatesGroup):
    f_name = State()
    l_name = State()
    date = State()
    time = State()
    num_of_people = State()