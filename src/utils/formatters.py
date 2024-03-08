from src.token import TokenPool
from src.nft import NftCollection, NftItem


def format_token_data(token_pool: TokenPool) -> str:
    token_data_msg = f'DEX: {token_pool.dex}\n'\
                     f'Pool: {token_pool.pool_name}\n'\
                     f'Price: 💎{token_pool.price_native:.4f} TON (💲{token_pool.price_usd:.4f})\n'

    return token_data_msg


def format_nft_collection(nft_collection: NftCollection) -> str:
    nft_collection_msg = f'Название: <b>{nft_collection.name}</b>\n'\
                         f'Адрес коллекции: <code>{nft_collection.address.to_str(is_user_friendly=True)}</code>\n'\
                         f'Адрес владельца: <code>{nft_collection.owner.to_str(is_user_friendly=True)}</code>\n\n'\
                         f'{nft_collection.description}\n\n'\
                         f'Количество холдеров: <b>{nft_collection.stats.holders_count}</b>\n'\
                         f'Количество NFT в коллекции: <b>{nft_collection.stats.items_count}</b>\n'\
                         f'Цена флора: 💎<b>{nft_collection.stats.floor_price}</b>\n'\
                         f'Объем торгов: 💎<b>{nft_collection.stats.total_volume / 10 ** 9:.2f}</b>\n\n'\
                         f'Ссылки: '\
                         f'{nft_collection.socials}'

    return nft_collection_msg


def format_nft_item(nft_item: NftItem) -> str:
    nft_item_msg = f'Название: <b>{nft_item.name}</b>\n'\
                   f'Коллекция: <b>{nft_item.collection.name}</b>\n\n'\
                   f'Адрес NFT: <code>{nft_item.address.to_str(is_user_friendly=True)}</code>\n'\
                   f'Адрес владельца: <code>{nft_item.owner_address}</code>'

    return nft_item_msg
