from aiogram.dispatcher.filters.state import State, StatesGroup


class BookingStates(StatesGroup):
    f_name = State()
    l_name = State()
    date = State()
    time = State()
    num_of_people = State()
    editing = State()


class BookingEdit(StatesGroup):
    fname_edit = State()
    lname_edit = State()
    date_edit = State()
    time_edit = State()
    ppl_edit = State()
    editing = State()