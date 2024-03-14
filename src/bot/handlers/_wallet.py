from aiogram import Router, F, types

from src.bot.keyboards import MenuCallbackFactory


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.page == 'wallet'))
async def wallet_menu(callback: types.CallbackQuery, callback_data: MenuCallbackFactory):
    await callback.message.answer(text='Функция пока не доступна')
