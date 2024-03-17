from aiogram import types

from src.utils import messages as msg
from src.bot.keyboards import return_menu_kb


async def on_unknown_intent(event: types.ErrorEvent, *args):
    await event.update.callback_query.message.delete()
    await event.update.callback_query.message.answer(text=msg.error, reply_markup=return_menu_kb())