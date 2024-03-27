import operator
import asyncio

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format

from ._states import AppStates
from src.utils import messages as msg
from src.services.app import app_service
from src.bot.keyboards import categories_kb, app_urls_kb
from src.utils.formatters import format_app


router = Router()


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'apps': dialog_manager.start_data.get('apps', None)
    }


async def on_app_selected(callback: types.CallbackQuery, s_btn: Select, dm: DialogManager, item_id: str):
    selected_app = dm.start_data['apps'][int(item_id)][1]

    app = await app_service.get_app(app_name=selected_app)

    m = format_app(app)
    img = types.URLInputFile(app.img)

    await asyncio.sleep(1)

    await callback.message.delete()
    try:
        await callback.message.answer_photo(photo=img, caption=m, reply_markup=app_urls_kb(app))
    except (AssertionError, TelegramBadRequest):
        await callback.message.answer(text=m, reply_markup=app_urls_kb(app))

    await dm.done()


async def cancel_handler(callback: types.CallbackQuery, *_):
    await callback.message.delete()
    await callback.message.answer(text=msg.app, reply_markup=categories_kb(app_service.categories))


async def back_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await dm.switch_to(state=AppStates.app)


dialog = Dialog(
    Window(
        Const(msg.app_dialog_select_app),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='s_apps',
                item_id_getter=operator.itemgetter(0),
                items='apps',
                on_click=on_app_selected
            ),
            id='apps',
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        Cancel(Const('◀ Приложения'), on_click=cancel_handler),
        Cancel(Const('◀ Назад'), on_click=back_handler),
        getter=get_data,
        state=AppStates.app
    )
)
