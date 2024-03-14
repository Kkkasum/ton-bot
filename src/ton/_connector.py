from pytonconnect import TonConnect
from pytonconnect.storage import IStorage, DefaultStorage


def get_connector(chat_id: int):
    return TonConnect()
