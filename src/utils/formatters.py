from src.services.jetton import Token, DEXPools
from src.services.nft import NftCollection, NftItem, SelectNftItem
from src.services.app import App


def format_connection(url: str) -> str:
    connection_msg = f'Воспользуйся <a href="{url}">этой ссылкой</a> для подключения или QR-кодом сверху'

    return connection_msg


def format_jetton_info(jetton: Token) -> str:
    jetton_info_msg = f'Название: <b>{jetton.name}</b> (<b>{jetton.symbol}</b>)\n'\
                      f'Адрес контракта: <code>{jetton.address.to_str()}</code>\n\n'\
                      f'Общая эмиссия (Supply): <b>{jetton.supply:.2f}</b>\n'\
                      f'Количество холдеров: <b>{jetton.holders_count}</b>\n'\

    return jetton_info_msg


def format_dex_pools(dex_pools: DEXPools) -> str:
    dex_pools_msg = '\n\n'.join([
                        f'<b>{pool.name}</b>\n'
                        f'Дата создания: <b>{pool.creation_datetime}</b>\n'
                        f'Цена {pool.main_jetton}: 💎<b>{pool.price_native:.4f}</b> (💲<b>{pool.price_usd:.4f}</b>)'
                        for pool in dex_pools.pools
                    ])

    return dex_pools_msg


def format_nft_collection(nft_collection: NftCollection) -> str:
    nft_collection_msg = f'Название: <b>{nft_collection.name}</b>\n'\
                         f'Адрес коллекции: <code>{nft_collection.address.to_str()}</code>\n'\
                         f'Адрес владельца: <code>{nft_collection.owner.to_str()}</code>\n\n'\
                         f'{nft_collection.description}\n\n'\
                         f'Количество холдеров: <b>{nft_collection.stats.holders_count}</b>\n'\
                         f'Количество NFT в коллекции: <b>{nft_collection.stats.items_count}</b>\n'\
                         f'Цена флора: 💎<b>{nft_collection.stats.floor_price}</b>\n'\
                         f'Объем торгов: 💎<b>{nft_collection.stats.volume:.2f}</b>\n\n'\
                         f'Ссылки: '\
                         f'{"отсутствуют" if not nft_collection.socials else nft_collection.socials}'

    return nft_collection_msg


def format_nft_item(nft_item: NftItem) -> str:
    nft_item_msg = f'Название: <b>{nft_item.name}</b>\n'\
                   f'Коллекция: <b>{nft_item.collection.name}</b>\n\n'\
                   f'Адрес NFT: <code>{nft_item.address.to_str()}</code>\n'\
                   f'Адрес владельца: <code>{"отсутствует" if not nft_item.owner else nft_item.owner_address}</code>'

    return nft_item_msg


def format_dialog_nft_item(nft_item: SelectNftItem) -> str:
    nft_item_msg = f'Название: <b>{nft_item.name}</b>\n'\
                   f'Адрес NFT: <code>{nft_item.address}</code>'

    return nft_item_msg


def format_app(app: App) -> str:
    app_msg = f'\t<b>{app.name}</b>\n\n'\
              f'Категория: <b>{app.category.value}</b>\n\n'\
              f'{app.description}'

    return app_msg
