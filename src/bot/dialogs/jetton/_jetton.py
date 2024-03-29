import operator
import asyncio

from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from pytoniq_core import Address

from ._states import JettonStates
from src.common import r
from src.utils import messages as msg
from src.utils.formatters import format_jetton_info
from src.services.jetton import jetton_service
from src.bot.keyboards import jetton_info_kb, jetton_kb


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'jettons': dialog_manager.start_data.get('jettons', None),
    }


async def on_jetton_selected(callback: types.CallbackQuery, s_btn: Select, dm: DialogManager, item_id: str):
    selected_jetton = dm.start_data['jettons'][int(item_id)]

    jetton_addr = Address(selected_jetton.address)

    jetton = await jetton_service.get_jetton_by_address(jetton_addr)

    m = format_jetton_info(jetton)
    img = types.URLInputFile(jetton.img)

    await asyncio.sleep(1)

    await callback.message.delete()
    try:
        await callback.message.answer_photo(photo=img, caption=m, reply_markup=jetton_info_kb(jetton_addr))
    except (AssertionError, TelegramBadRequest):
        await callback.message.answer(text=m, reply_markup=jetton_info_kb(jetton_addr))

    await r.set(name=callback.from_user.id, value=jetton_addr.to_str(is_user_friendly=False))

    await dm.done()


async def cancel_handler(callback: types.CallbackQuery, *_):
    await callback.message.delete()
    await callback.message.answer(text=msg.jetton, reply_markup=jetton_kb())


dialog = Dialog(
    Window(
        Const(msg.jetton_dialog_select_jetton),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='s_jettons',
                item_id_getter=operator.itemgetter(0),
                items='jettons',
                on_click=on_jetton_selected
            ),
            id='jettons',
            width=1,
            height=5,
            hide_on_single_page=True,
        ),
        Cancel(Const('◀ Jetton'), on_click=cancel_handler),
        getter=get_data,
        state=JettonStates.symbol
    )
)
