from aiogram import Router, types
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text='some')
