from aiogram.fsm.state import StatesGroup, State


class TransferStates(StatesGroup):
    address = State()
    toncoin_amount = State()
    finish = State()
