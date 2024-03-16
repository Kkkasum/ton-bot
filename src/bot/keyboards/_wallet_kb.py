from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from ._menu_kb import MenuCallbackFactory


class WalletCallbackFactory(CallbackData, prefix='wallets'):
    index: int


class WalletConnectionCallbackFactory(CallbackData, prefix='wallet'):
    action: str


def wallets_kb(wallets: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.button(text=wallet, callback_data=WalletCallbackFactory(index=index))
        for index, wallet in enumerate(wallets)
    ]
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallet_try_again_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Попробовать подключить еще раз', callback_data=MenuCallbackFactory(page='wallet'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallet_connect_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Привязать кошелек', callback_data=WalletConnectionCallbackFactory(action='connect'))

    return builder.as_markup()


def wallet_connected_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Отвязать кошелек', callback_data=WalletConnectionCallbackFactory(action='disconnect'))

    return builder.as_markup()
