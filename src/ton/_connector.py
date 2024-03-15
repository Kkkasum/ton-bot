from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage

from src.common import config


def get_connector(user_id: int) -> TonConnect:
    storage = FileStorage(f'connections/{user_id}.json')
    return TonConnect(manifest_url=config.MANIFEST_URL, storage=storage, wallets_list_source=config.WALLETS_LIST_URL)
