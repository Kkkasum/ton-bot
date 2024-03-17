from aiogram.fsm.state import StatesGroup, State


class TransferStates(StatesGroup):
    address = State()
    token = State()
    jetton = State()
    token_amount = State()
    finish = State()
