from aiogram.dispatcher.filters.state import StatesGroup, State


class RequestForm(StatesGroup):
    purpose_q = State()
    place_q = State()
    date_q = State()
    comment_q = State()


class AcceptRequest(StatesGroup):
    accept = State()
