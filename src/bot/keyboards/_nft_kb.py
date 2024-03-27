from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters.callback_data import CallbackData

from ._menu_kb import MenuCallbackFactory
from src.services.nft import NftCollection, NftItem


class NftCallbackFactory(CallbackData, prefix='nft'):
    page: str


class NftCollectionHistoryCallbackFactory(CallbackData, prefix='nft_collection_history'):
    days: int


def nft_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='По адресу контракта', callback_data=NftCallbackFactory(page='by_contract'))
    builder.button(text='По названию', callback_data=NftCallbackFactory(page='by_name'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def nft_search_kb(by_contract: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Поиск коллекции', callback_data=NftCallbackFactory(page='search_collection'))

    if by_contract:
        builder.button(text='Поиск NFT', callback_data=NftCallbackFactory(page='search_nft'))

    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1, 1, 1)

    return builder.as_markup()


def nft_collection_kb(nft_collection: NftCollection) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Ссылка на GetGems.io',
        url=f'https://getgems.io/collection/{nft_collection.address.to_str(is_user_friendly=False)}'
    )  # getgems.io link

    builder.button(
        text='GetGems.io',
        web_app=WebAppInfo(url=f'https://getgems.io/collection/{nft_collection.address.to_str(is_user_friendly=False)}')
    )  # getgems.io web app

    builder.button(
        text='История продаж',
        callback_data=NftCallbackFactory(
            page='collection_history'
        ),
    )
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(2, 1)

    return builder.as_markup()


def nft_item_kb(nft_item: NftItem) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Ссылка на GetGems.io',
        url=f'https://getgems.io/collection/{nft_item.collection.address.to_str(is_user_friendly=False)}/'
            f'{nft_item.address.to_str()}'
    )  # getgems.io link

    builder.button(
        text='GetGems.io',
        web_app=WebAppInfo(
            url=f'https://getgems.io/collection/{nft_item.collection.address.to_str(is_user_friendly=False)}/'
                f'{nft_item.address.to_str()}'
        )
    )  # getgems.io web app

    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def nft_collection_history_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='За 1 день',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=1
        )
    )
    builder.button(
        text='За 7 дней',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=7
        )
    )
    builder.button(
        text='За 14 дней',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=14
        )
    )
    builder.button(
        text='За 30 дней',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=30
        )
    )
    builder.button(
        text='За 60 дней',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=60
        )
    )
    builder.button(
        text='За 90 дней',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=90
        )
    )
    builder.button(
        text='За последний год',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=365
        )
    )
    builder.button(
        text='За все время',
        callback_data=NftCollectionHistoryCallbackFactory(
            days=1000
        )
    )

    builder.adjust(3, 3, 2)

    return builder.as_markup()
