from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from pytoniq_core import Address, AddressError

from src.bot.middleware import AntifloodMiddleware
from src.common import r
from src.services.jetton import jettons
from src.utils import messages as msg
from src.utils.formatters import format_jetton_info, format_dex_pools
from src.bot.keyboards import (
    jetton_kb,
    jetton_info_kb,
    dexes_kb,
    MenuCallbackFactory,
    JettonCallbackFactory,
    DEXCallbackFactory
)


router = Router()
router.callback_query.middleware(AntifloodMiddleware())


@router.callback_query(MenuCallbackFactory.filter(F.page == 'jetton'))
async def jetton_menu(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.jetton, reply_markup=jetton_kb())


@router.callback_query(JettonCallbackFactory.filter())
async def jetton_callback(callback: types.CallbackQuery, callback_data: JettonCallbackFactory, state: FSMContext):
    if callback_data.page == 'contract':
        await callback.message.edit_text(text=msg.jetton_contract)
        await state.set_state('jetton_contract')

    if callback_data.page == 'name':
        await callback.message.edit_text(text=msg.jetton_name)
        await state.set_state('jetton_name')

    if callback_data.page == 'dexes':
        dexes = await jettons.get_dexes()
        await callback.message.answer(text=msg.jetton_dexes, reply_markup=dexes_kb(dexes))


@router.message(StateFilter('jetton_contract'))
async def jetton_contract(message: types.Message, state: FSMContext):
    try:
        jetton_addr = Address(message.text)

        jetton_info = await jettons.get_jetton_info(jetton_addr)

        m = format_jetton_info(jetton_info)
        img = types.URLInputFile(jetton_info.img)

        try:
            await message.answer_photo(photo=img, caption=m, reply_markup=jetton_info_kb(jetton_addr))
        except (AssertionError, TelegramBadRequest):
            await message.answer(text=m, reply_markup=jetton_info_kb(jetton_addr))

        await r.set(name=message.from_user.id, value=jetton_addr.to_str(is_user_friendly=False))
        await state.clear()
    except (AddressError, ValueError):
        await message.answer(text=msg.jetton_contract_error)
        await message.answer(text=msg.jetton_contract)


@router.message(StateFilter('jetton_name'))
async def jetton_name(message: types.Message):
    pass


@router.callback_query(DEXCallbackFactory.filter())
async def dex_callback(callback: types.CallbackQuery, callback_data: DEXCallbackFactory):
    jetton_addr = Address(str(await r.getdel(name=callback.from_user.id), 'utf-8'))
    dex_pools = await jettons.get_dex_pools(callback_data.dex, jetton_addr)

    m = format_dex_pools(dex_pools)
    await callback.message.edit_text(text=m)
