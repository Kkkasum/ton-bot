import asyncio
from typing import Callable, Awaitable, Any
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from src.common import r
from src.utils import messages as msg


class AntifloodMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.CallbackQuery,
        data: dict[str, Any]
    ):
        now = datetime.utcnow()
        last_message = await r.getset(name=data['event_from_user'].username, value=now.strftime('%Y-%m-%d %H:%M:%S'))

        try:
            delta = now - datetime.strptime(str(last_message, 'utf-8'), '%Y-%m-%d %H:%M:%S')
            if delta > timedelta(seconds=0.5):
                return await handler(event, data)
        except TypeError:
            return await handler(event, data)

        await event.answer(text=msg.antiflood, show_alert=True)
        return
