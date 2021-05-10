from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationForm(StatesGroup):
    first_name_q = State()
    last_name_q = State()
    position_q = State()
    workplace_q = State()


