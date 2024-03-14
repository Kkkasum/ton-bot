from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 1, prefix='antiflood_'):
        self.rate_limit = rate_limit
        self.prefix = prefix
        super(ThrottlingMiddleware, self).__init__()

    async def __call__(self):
        pass
