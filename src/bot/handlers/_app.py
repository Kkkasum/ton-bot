from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.utils import messages as msg
from src.bot.keyboards import app_kb, AppCallbackFactory, MenuCallbackFactory


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.page == 'app'))
async def app_menu(callback: types.CallbackQuery, callback_data: MenuCallbackFactory):
    await callback.message.answer(text=msg.app, reply_markup=app_kb())


@router.callback_query(AppCallbackFactory.filter())
async def app_callback(callback: types.CallbackQuery, callback_data: AppCallbackFactory):
    if callback_data.page == 'wallets':
        pass

    if callback_data.page == 'defi':
        pass

    if callback_data.page == 'nfts':
        pass

    if callback_data.page == 'gamefi':
        pass

    if callback_data.page == 'utility':
        pass


@router.message(StateFilter('wallets'))
async def wallets(message: types.Message, state: FSMContext):
    pass
