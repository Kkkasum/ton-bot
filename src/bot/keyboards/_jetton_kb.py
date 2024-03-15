from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters.callback_data import CallbackData

from pytoniq_core import Address

from ._menu_kb import MenuCallbackFactory
from src.jetton import DEX


class JettonCallbackFactory(CallbackData, prefix='jetton'):
    page: str


class DEXCallbackFactory(CallbackData, prefix='dex'):
    dex: str


def jetton_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='По адресу контракта', callback_data=JettonCallbackFactory(page='contract'))
    builder.button(text='По названию', callback_data=JettonCallbackFactory(page='name'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def jetton_info_kb(jetton_addr: Address) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='DeDust.io',
        web_app=WebAppInfo(url=f'https://dedust.io/swap/{jetton_addr.to_str(is_user_friendly=False)}/TON')
    )
    builder.button(
        text='Ston.fi',
        web_app=WebAppInfo(url=f'https://app.ston.fi/swap?ft={jetton_addr.to_str(is_user_friendly=False)}&tt=TON')
    )
    builder.button(
        text='DeDust.io',
        url=f'https://dedust.io/swap/{jetton_addr.to_str(is_user_friendly=False)}/TON'
    )
    builder.button(
        text='Ston.fi',
        url=f'https://app.ston.fi/swap?ft={jetton_addr.to_str(is_user_friendly=False)}&tt=TON'
    )
    builder.button(
        text='Tonviewer',
        web_app=WebAppInfo(url=f'https://tonviewer.com/{jetton_addr.to_str()}')
    )
    builder.button(text='Посмотреть доступные пулы', callback_data=JettonCallbackFactory(page='dexes'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(2, 2, 1)

    return builder.as_markup()


def dexes_kb(dexes: list[DEX]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.button(text=dex.name, callback_data=DEXCallbackFactory(dex=dex.id))
        for dex in dexes
    ]

    return builder.as_markup()
