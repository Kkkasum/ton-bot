from aiogram.fsm.state import StatesGroup, State


class TransferStates(StatesGroup):
    address = State()
    token = State()
    jetton = State()
    amount = State()
    comment = State()
    finish = State()
