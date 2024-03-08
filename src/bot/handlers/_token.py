from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from pytoniq_core import Address, AddressError

from src.bot.keyboards import token_kb, TokenCallbackFactory
from src.token import jetton
from src.utils import messages as msg
from src.utils.formatters import format_token_data


router = Router()


@router.message(Command('token'))
async def token(message: types.Message):
    await message.answer(text=msg.token_msg, reply_markup=token_kb())


@router.callback_query(TokenCallbackFactory.filter())
async def token_callback(callback: types.CallbackQuery, callback_data: TokenCallbackFactory, state: FSMContext):
    if callback_data.type == 'contract':
        await callback.message.edit_text(text=msg.token_contract_msg)
        await state.set_state('token_contract')

    if callback_data.type == 'name':
        await callback.message.edit_text(text=msg.token_name_msg)
        await state.set_state('token_name')


@router.message(StateFilter('token_contract'))
async def token_contract(message: types.Message, state: FSMContext):
    try:
        token_addr = Address(message.text)
        token_pools = await jetton.get_token_pools_by_contract(token_addr)

        for token_pool in token_pools:
            m = format_token_data(token_pool)
            await message.answer(text=m)
        await state.clear()
    except AddressError:
        await message.answer(text=msg.token_contract_error_msg)
        await message.answer(text=msg.token_contract_msg)


@router.message(StateFilter('token_name'))
async def token_name(message: types.Message):
    pass

