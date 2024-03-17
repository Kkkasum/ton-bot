from typing import Any
from base64 import urlsafe_b64encode

from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage

from pytoniq_core import begin_cell

from src.common import config


def get_connector(user_id: int) -> TonConnect:
    storage = FileStorage(f'connections/{user_id}.json')
    return TonConnect(manifest_url=config.MANIFEST_URL, storage=storage, wallets_list_source=config.WALLETS_LIST_URL)


def ton_transfer(destination_addr: str, amount: int, comment: str) -> dict[str, Any]:
    data = {
        'address': destination_addr,
        'amount': str(amount * 10 ** 9),
        'payload': urlsafe_b64encode(
            begin_cell()
            .store_uint(0, 32)
            .store_string(comment)
            .end_cell()
            .to_boc()
        )
        .decode()
    }

    return data
