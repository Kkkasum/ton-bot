from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class AppCallbackFactory(CallbackData, prefix='app'):
    page: str


def app_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Wallets',
        callback_data=AppCallbackFactory(page='wallets')
    )
    builder.button(
        text='DeFi',
        callback_data=AppCallbackFactory(page='defi')
    )
    builder.button(
        text='NFT',
        callback_data=AppCallbackFactory(page='nft')
    )
    builder.button(
        text='GameFi',
        callback_data=AppCallbackFactory(page='gamefi')
    )
    builder.button(
        text='TON Utility',
        callback_data=AppCallbackFactory(page='utility')
    )

    return builder.as_markup()


def wallets_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    return builder.as_markup()