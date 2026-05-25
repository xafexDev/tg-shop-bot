from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_address = State()
    waiting_confirm = State()
