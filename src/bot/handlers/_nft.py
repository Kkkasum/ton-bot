from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from pytoniq_core import Address, AddressError

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
    NftCallbackFactory,
    NftCollectionHistoryCallbackFactory
)


router = Router()


@router.message(Command('nft'))
async def nft(message: types.Message):
    await message.answer(text=msg.nft_msg, reply_markup=nft_kb())


@router.callback_query(NftCallbackFactory.filter())
async def nft_callback(callback: types.CallbackQuery, callback_data: NftCallbackFactory, state: FSMContext):
    if callback_data.page == 'contract':
        await callback.message.edit_text(text=msg.nft_search_msg, reply_markup=nft_search_kb(by_contract=True))

    if callback_data.page == 'name':
        await callback.message.edit_text(text=msg.nft_search_msg, reply_markup=nft_search_kb(by_contract=False))

    if callback_data.page == 'search_collection':
        await callback.message.edit_text(text=msg.nft_search_collection_msg)
        await state.set_state('search_collection')

    if callback_data.page == 'search_nft':
        await callback.message.edit_text(text=msg.nft_search_nft_msg)
        await state.set_state('search_nft')

    if callback_data.page == 'collection_history':
        collection_addr = Address(await r.get(name=str(callback.from_user.id)))
        print(collection_addr.to_str())
        await callback.message.edit_text(
            text=msg.nft_collection_history_msg,
            reply_markup=nft_collection_history(collection_addr.to_str())
        )


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
        await state.clear()
    except AddressError:
        await message.answer(text=msg.nft_contract_error_msg)
        await message.answer(text=msg.nft_search_collection_msg)


@router.message(StateFilter('search_nft'))
async def search_nft(message: types.Message, state: FSMContext):
    try:
        collection_addr = Address(message.text)
        nft_item = await nft_tonapi.get_nft_item(collection_addr)

        m = format_nft_item(nft_item)
        img = types.URLInputFile(nft_item.img)

        try:
            await message.answer_photo(photo=img, caption=m, reply_markup=nft_item_kb(nft_item))
            await r.set(name=str(message.from_user.id), value=collection_addr.to_str())
        except (AssertionError, TelegramBadRequest):
            await message.answer(text=m, reply_markup=nft_item_kb(nft_item))
        await state.clear()
    except AddressError:
        await message.answer(text=msg.nft_contract_error_msg)
        await message.answer(text=msg.nft_search_collection_msg)


@router.message(NftCollectionHistoryCallbackFactory.filter())
async def collection_history(callback: types.CallbackQuery, callback_data: NftCollectionHistoryCallbackFactory):
    collection_addr = Address(await r.get(name=str(callback.from_user.id)))
    print(collection_addr.to_str())
    history = await gg.get_collection_sales_history(collection_addr=collection_addr, days_count=callback_data.days)
    print(history)
