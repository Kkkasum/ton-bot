from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from ._menu_kb import MenuCallbackFactory


class ContractCallbackFactory(CallbackData, prefix='contract'):
    page: str


class CategoryCallbackFactory(CallbackData, prefix='category'):
    page: str


class StandardContractCallbackFactory(CallbackData, prefix='standard_contract'):
    page: str


def contract_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Поиск шаблона для смарт-контракта', callback_data=ContractCallbackFactory(page='templates'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def contract_templates_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Jetton Contracts', callback_data=CategoryCallbackFactory(page='jetton'))
    builder.button(text='NFT Contracts', callback_data=CategoryCallbackFactory(page='nft'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def contract_category_jetton_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Jetton Minter Contract (Jetton Master Contract)',
        callback_data=StandardContractCallbackFactory(page='jetton-minter')
    )
    builder.button(
        text='Jetton Wallet Contract',
        callback_data=StandardContractCallbackFactory(page='jetton-wallet')
    )
    builder.button(
        text='☰ Главное меню',
        callback_data=MenuCallbackFactory(page='menu')
    )

    builder.adjust(1)

    return builder.as_markup()


def contract_category_nft_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='NFT Collection Contract',
        callback_data=StandardContractCallbackFactory(page='nft-collection')
    )
    builder.button(
        text='NFT Item Contract',
        callback_data=StandardContractCallbackFactory(page='nft-item')
    )
    builder.button(
        text='NFT Marketplace Contract',
        callback_data=StandardContractCallbackFactory(page='nft-marketplace')
    )
    builder.button(
        text='NFT Sale Contract',
        callback_data=StandardContractCallbackFactory(page='nft-sale')
    )
    builder.button(
        text='☰ Главное меню',
        callback_data=MenuCallbackFactory(page='menu')
    )

    builder.adjust(1)

    return builder.as_markup()
