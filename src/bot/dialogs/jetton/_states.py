from aiogram.fsm.state import StatesGroup, State


class JettonStates(StatesGroup):
    symbol = State()

