from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from ._menu_kb import MenuCallbackFactory


class WalletCallbackFactory(CallbackData, prefix='wallets'):
    index: int


class WalletActionCallbackFactory(CallbackData, prefix='wallet_actions'):
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


def wallet_actions_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Сделать перевод', callback_data=WalletActionCallbackFactory(action='transfer'))
    builder.button(text='Отключить кошелек', callback_data=WalletActionCallbackFactory(action='disconnect'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallet_return_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='💰 Кошелек', callback_data=MenuCallbackFactory(page='wallet'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()
