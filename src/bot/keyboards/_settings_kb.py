from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class SettingsCallbackFactory(CallbackData, prefix='settings'):
    page: str


def settings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Поменять язык', callback_data=SettingsCallbackFactory(page='lang'))

    return builder.as_markup()


def lang_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Русский', callback_data=SettingsCallbackFactory(page='ru'))
    builder.button(text='English', callback_data=SettingsCallbackFactory(page='en'))

    return builder.as_markup()
