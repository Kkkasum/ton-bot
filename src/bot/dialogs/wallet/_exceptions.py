from aiogram import types

from src.utils import messages as msg
from src.bot.keyboards import return_wallet_kb


async def on_unknown_intent(event: types.ErrorEvent, *_):
    await event.update.callback_query.message.delete()
    await event.update.callback_query.message.answer(text=msg.error, reply_markup=return_wallet_kb())


async def on_unknown_state(event: types.ErrorEvent, *_):
    await event.update.callback_query.message.delete()
    await event.update.callback_query.message.answer(text=msg.error, reply_markup=return_wallet_kb())
