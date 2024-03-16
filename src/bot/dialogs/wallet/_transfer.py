from aiogram import Router, types

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row

from pytoniq_core import Address, AddressError

from ._states import TransferStates
from src.utils import messages as msg
from src.bot.keyboards import wallet_actions_kb, menu_kb


router = Router()


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        'address': dialog_manager.dialog_data.get('address', None),
        'toncoin_amount': dialog_manager.dialog_data.get('toncoin_amount', None)
    }


async def address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        address = Address(message.text)
    except AddressError:
        await message.answer(text=msg.wallet_address_error)

        await message.answer(text=msg.menu, reply_markup=wallet_actions_kb())

        await dm.done()
        return

    dm.dialog_data['address'] = address.to_str(is_user_friendly=True)

    await dm.next()


async def toncoin_amount_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        toncoin_amount = float(message.text)
    except ValueError:
        await message.answer(text=msg.wallet_toncoin_amount_error)
        await dm.done()
        return

    dm.dialog_data['toncoin_amount'] = toncoin_amount

    await dm.next()


async def cancel_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()
    await dm.done()

    await callback.message.answer(text=msg.menu, reply_markup=menu_kb())


async def confirm_transaction_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    pass


dialog = Dialog(
    Window(
        Const(msg.wallet_transfer_address),
        MessageInput(address_handler, content_types=[types.ContentType.TEXT]),
        state=TransferStates.address
    ),
    Window(
        Const(msg.wallet_transfer_toncoin_amount),
        MessageInput(toncoin_amount_handler, content_types=[types.ContentType.TEXT]),
        state=TransferStates.toncoin_amount
    ),
    Window(
        Multi(
            Format(msg.wallet_dialog_address),
            Format(msg.wallet_dialog_toncoin_amount),
            sep='\n'
        ),
        Row(
            Button(Const(msg.wallet_dialog_cancel_transfer), id='cancel', on_click=cancel_handler),
            Button(Const(msg.wallet_dialog_confirm_transfer), id='confirm', on_click=confirm_transaction_handler)
        ),
        getter=get_data,
        state=TransferStates.finish
    )
)
