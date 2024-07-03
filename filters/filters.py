from aiogram.fsm.state import StatesGroup, State


class ChooseFilter(StatesGroup):
    min_max = State()
    year_price_capacity = State()
    accept = State()
    add_params = State()
    via_link = State()
