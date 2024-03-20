from aiogram import Router, types, F

from src.bot.keyboards import settings_kb, lang_kb, menu_kb, MenuCallbackFactory, SettingsCallbackFactory
from src.utils import messages as msg


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.page == 'settings'))
async def settings_menu(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.settings, reply_markup=settings_kb())


@router.callback_query(SettingsCallbackFactory.filter(F.page == 'lang'))
async def lang_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.lang, reply_markup=lang_kb())


@router.callback_query(SettingsCallbackFactory.filter(F.page == 'ru'))
async def ru_lang_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text='Русский язык')

    await callback.message.answer(text=msg.menu, reply_markup=menu_kb())


@router.callback_query(SettingsCallbackFactory.filter(F.page == 'en'))
async def ru_lang_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text='English')

    await callback.message.answer(text=msg.menu, reply_markup=menu_kb())
