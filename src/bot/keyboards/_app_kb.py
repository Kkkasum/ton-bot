from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters.callback_data import CallbackData

from src.bot.keyboards import MenuCallbackFactory
from src.services.app import App


class AppCategoryCallbackFactory(CallbackData, prefix='category'):
    page: str


def categories_kb(categories: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.button(
            text=category,
            callback_data=AppCategoryCallbackFactory(page=category.lower())
        )
        for category in categories
    ]
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def app_urls_kb(app: App) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=app.name,
        url=app.url
    )
    builder.button(
        text='Ton Apps',
        web_app=WebAppInfo(url=f'https://ton.app/wallets/{app.name}')
    )
    builder.button(text='📱 Приложения', callback_data=MenuCallbackFactory(page='app'))

    builder.adjust(2)

    return builder.as_markup()
