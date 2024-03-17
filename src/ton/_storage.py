from pytonconnect.storage import IStorage

from src.common import r


class TcStorage(IStorage):

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def _get_key(self, key: str):
        return str(self.chat_id) + key

    async def set_item(self, key: str, value: str):
        await r.set(name=self._get_key(key), value=value)

    async def get_item(self, key: str, default_value: str = None):
        value = await r.get(name=self._get_key(key))
        return value.decode() if value else default_value

    async def remove_item(self, key: str):
        await r.delete(self._get_key(key))
