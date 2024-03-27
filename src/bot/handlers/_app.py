from aiogram import Router, F, types

from aiogram_dialog import DialogManager, StartMode

from src.utils import messages as msg
from src.services.app import app_service
from src.bot.keyboards import categories_kb, AppCategoryCallbackFactory, MenuCallbackFactory
from src.bot.dialogs import include_app_dialog, AppStates


router = Router()
include_app_dialog(router)


@router.callback_query(MenuCallbackFactory.filter(F.page == 'app'))
async def app_menu(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.app, reply_markup=categories_kb(app_service.categories))


@router.callback_query(AppCategoryCallbackFactory.filter())
async def app_category_callback(callback: types.CallbackQuery, dialog_manager: DialogManager, callback_data: AppCategoryCallbackFactory):
    await dialog_manager.start(
        state=AppStates.app,
        data={
            'category': callback_data.page,
            'apps': await app_service.get_apps_by_category(category=callback_data.page)
        },
        mode=StartMode.RESET_STACK
    )
