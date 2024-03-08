from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class TokenCallbackFactory(CallbackData, prefix='token'):
    type: str


def token_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='По адресу контракта', callback_data=TokenCallbackFactory(type='contract'))
    builder.button(text='По названию', callback_data=TokenCallbackFactory(type='name'))

    return builder.as_markup()
