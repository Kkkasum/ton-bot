from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from pytoniq_core import Address, AddressError

from src.bot.middleware import AntifloodMiddleware
from src.nft import nft_tonapi, gg
from src.common import r
from src.utils import messages as msg
from src.utils.formatters import format_nft_collection, format_nft_item
from src.bot.keyboards import (
    nft_kb,
    nft_search_kb,
    nft_collection_kb,
    nft_item_kb,
    nft_collection_history,
    MenuCallbackFactory,
    NftCallbackFactory,
    NftCollectionHistoryCallbackFactory
)


router = Router()
router.callback_query.middleware(AntifloodMiddleware())


@router.callback_query(MenuCallbackFactory.filter(F.page == 'nft'))
async def nft_menu(callback: types.CallbackQuery, callback_data: MenuCallbackFactory):
    await callback.message.edit_text(text=msg.nft, reply_markup=nft_kb())


@router.callback_query(NftCallbackFactory.filter())
async def nft_callback(callback: types.CallbackQuery, callback_data: NftCallbackFactory, state: FSMContext):
    if callback_data.page == 'contract':
        await callback.message.edit_text(text=msg.nft_search, reply_markup=nft_search_kb(by_contract=True))

    if callback_data.page == 'name':
        await callback.message.edit_text(text=msg.nft_search, reply_markup=nft_search_kb(by_contract=False))

    if callback_data.page == 'search_collection':
        await callback.message.edit_text(text=msg.nft_search_collection)
        await state.set_state('search_collection')

    if callback_data.page == 'search_nft':
        await callback.message.edit_text(text=msg.nft_search_nft)
        await state.set_state('search_nft')

    if callback_data.page == 'collection_history':
        await callback.message.answer(text=msg.nft_collection_history, reply_markup=nft_collection_history())


@router.message(StateFilter('search_collection'))
async def search_collection(message: types.Message, state: FSMContext):
    try:
        collection_addr = Address(message.text)
        nft_collection = await gg.get_nft_collection(collection_addr)

        m = format_nft_collection(nft_collection)
        img = types.URLInputFile(nft_collection.img)

        try:
            await message.answer_photo(photo=img, caption=m, reply_markup=nft_collection_kb(nft_collection))
        except (AssertionError, TelegramBadRequest):
            await message.answer(text=m, reply_markup=nft_collection_kb(nft_collection))

        await r.set(name=message.from_user.id, value=collection_addr.to_str(is_user_friendly=False))
        await state.clear()
    except AddressError:
        await message.answer(text=msg.nft_contract_error)
        await message.answer(text=msg.nft_search_collection)


@router.message(StateFilter('search_nft'))
async def search_nft(message: types.Message, state: FSMContext):
    try:
        collection_addr = Address(message.text)
        nft_item = await nft_tonapi.get_nft_item(collection_addr)

        m = format_nft_item(nft_item)
        img = types.URLInputFile(nft_item.img)

        try:
            await message.answer_photo(photo=img, caption=m, reply_markup=nft_item_kb(nft_item))
        except (AssertionError, TelegramBadRequest):
            await message.answer(text=m, reply_markup=nft_item_kb(nft_item))

        await state.clear()
    except AddressError:
        await message.answer(text=msg.nft_contract_error)
        await message.answer(text=msg.nft_search_collection)


@router.callback_query(NftCollectionHistoryCallbackFactory.filter())
async def collection_history(callback: types.CallbackQuery, callback_data: NftCollectionHistoryCallbackFactory):
    collection_addr = Address(str(await r.getdel(name=callback.from_user.id), 'utf-8'))
    history = await gg.get_collection_sales_history(collection_addr=collection_addr, days_count=callback_data.days)
