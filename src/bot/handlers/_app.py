from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from src.utils import messages as msg
from src.bot.keyboards import app_kb, AppCallbackFactory


router = Router()


@router.message(Command('app'))
async def app(message: types.Message):
    await message.answer(text=msg.app_msg, reply_markup=app_kb())


@router.callback_query(AppCallbackFactory.filter())
async def app_callback(callback: types.CallbackQuery, callback_data: AppCallbackFactory):
    if callback_data.page == 'wallets':
        pass

    if callback_data.page == 'defi':
        pass

    if callback_data.page == 'nft':
        pass

    if callback_data.page == 'gamefi':
        pass

    if callback_data.page == 'utility':
        pass


@router.message(StateFilter('wallets'))
async def wallets(message: types.Message, state: FSMContext):
    pass
