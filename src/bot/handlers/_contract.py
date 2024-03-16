from aiogram import Router, types, F

from src.utils import messages as msg
from src.contract import contract
from src.bot.keyboards import (
    contract_kb,
    contract_templates_kb,
    contract_category_jetton_kb,
    contract_category_nft_kb,
    MenuCallbackFactory,
    ContractCallbackFactory,
    CategoryCallbackFactory,
    StandardContractCallbackFactory
)


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.page == 'contract'))
async def contract_menu(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text=msg.contract, reply_markup=contract_kb())


@router.callback_query(ContractCallbackFactory.filter(F.page == 'templates'))
async def contract_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text=msg.contract_category, reply_markup=contract_templates_kb())


@router.callback_query(CategoryCallbackFactory.filter())
async def category_callback(callback: types.CallbackQuery, callback_data: CategoryCallbackFactory):
    if callback_data.page == 'jetton':
        await callback.message.edit_text(text=msg.contract_templates_jetton, reply_markup=contract_category_jetton_kb())

    if callback_data.page == 'nft':
        await callback.message.edit_text(text=msg.contract_templates_nft, reply_markup=contract_category_nft_kb())


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'jetton-minter'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'jetton-wallet'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'nft-collection'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'nft-item'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'nft-marketplace'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')


@router.callback_query(StandardContractCallbackFactory.filter(F.page == 'nft-sale'))
async def template_jetton_minter_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text='jetton-minter')
