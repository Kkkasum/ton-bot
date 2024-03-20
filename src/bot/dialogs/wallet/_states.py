from aiogram.fsm.state import StatesGroup, State


class TransferStates(StatesGroup):
    address = State()
    token = State()
    jetton = State()
    amount = State()
    nft = State()
    nft_address = State()
    available_nft_items = State()
    comment = State()
    finish = State()
