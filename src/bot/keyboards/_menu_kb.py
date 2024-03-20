from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class MenuCallbackFactory(CallbackData, prefix='menu'):
    page: str


def menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='💰 Кошелек', callback_data=MenuCallbackFactory(page='wallet'))
    builder.button(text='💎 Jetton', callback_data=MenuCallbackFactory(page='jetton'))
    builder.button(text='🖼 NFT', callback_data=MenuCallbackFactory(page='nft'))
    builder.button(text='📱 Приложения TON', callback_data=MenuCallbackFactory(page='app'))
    builder.button(text='Контракты', callback_data=MenuCallbackFactory(page='contract'))
    builder.button(text='⚙️ Настройки', callback_data=MenuCallbackFactory(page='settings'))

    builder.adjust(1)

    return builder.as_markup()


def return_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    return builder.as_markup()
