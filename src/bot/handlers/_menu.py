from aiogram import Router, F, types
from aiogram.filters import CommandStart

from src.bot.keyboards import menu_kb, MenuCallbackFactory
from src.utils import messages as msg


router = Router()


@router.message(CommandStart())
async def menu(message: types.Message):
    await message.answer(text=msg.menu, reply_markup=menu_kb())


@router.callback_query(MenuCallbackFactory.filter(F.page == 'menu'))
async def menu_callback(callback: types.CallbackQuery, **_):
    await callback.message.edit_text(text=msg.menu, reply_markup=menu_kb())
