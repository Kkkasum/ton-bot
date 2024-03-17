from time import time

from aiogram import Router, types

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Row, Cancel

from pytoniq_core import Address, AddressError

from pytonconnect.exceptions import UserRejectsError

from ._states import TransferStates
from src.utils import messages as msg
from src.bot.keyboards import wallet_actions_kb, return_menu_kb
from src.ton import get_connector, ton_transfer


router = Router()


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'address': dialog_manager.dialog_data.get('address', None),
        'token': dialog_manager.dialog_data.get('token', None),
        'token_amount': dialog_manager.dialog_data.get('token_amount', None)
    }


async def address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager, **kwargs):
    try:
        address = Address(message.text)
    except (AddressError, ValueError):
        await message.answer(text=msg.wallet_address_error)

        await message.answer(text=msg.menu, reply_markup=wallet_actions_kb())

        await dm.done()
        return

    dm.dialog_data['address'] = address.to_str(is_user_friendly=True)

    await dm.next()


async def token_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()

    dm.dialog_data['token'] = button.text.text

    await dm.switch_to(state=TransferStates.token_amount)


async def token_amount_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        token_amount = float(message.text)
    except ValueError:
        await message.answer(text=msg.wallet_toncoin_amount_error)
        await dm.done()
        return

    dm.dialog_data['token_amount'] = token_amount

    await dm.next()


async def cancel_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


async def confirm_transaction_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = get_connector(callback.from_user.id)

    is_connected = await connector.restore_connection()
    if not is_connected:
        await callback.message.answer(text=msg.wallet_not_connected)
        await callback.message.answer(text=msg.menu, reply_markup=return_menu_kb())
        return

    transfer = ton_transfer(dm.dialog_data['address'], dm.dialog_data['token_amount'], 'asd')

    transaction = {
        'valid_until': int(time() + 3600),
        'messages': [
            transfer
        ]
    }

    approve_msg = await callback.message.answer(text='approve')

    try:
        await connector.send_transaction(transaction=transaction)
    except UserRejectsError:
        await approve_msg.delete()
        await callback.message.answer(text=msg.wallet_dialog_rejected_transfer)


dialog = Dialog(
    Window(
        Const(msg.wallet_dialog_address_input),
        MessageInput(address_handler, content_types=[types.ContentType.TEXT]),
        state=TransferStates.address
    ),
    Window(
        Const(msg.wallet_dialog_token),
        Row(
            Button(Const('TON'), id='ton', on_click=token_handler),
            SwitchTo(Const('Jetton'), id='jetton', state=TransferStates.jetton)
        ),
        state=TransferStates.token
    ),
    Window(
        Const(msg.wallet_dialog_jetton),
        Row(
            Button(Const('DFC'), id='dfc', on_click=token_handler),
            Button(Const('TONNEL'), id='tonnel', on_click=token_handler)
        ),
        state=TransferStates.jetton
    ),
    Window(
        Format(msg.wallet_dialog_token_amount_input),
        MessageInput(token_amount_handler, content_types=[types.ContentType.TEXT]),
        getter=get_data,
        state=TransferStates.token_amount
    ),
    Window(
        Multi(
            Format(msg.wallet_dialog_address),
            Format(msg.wallet_dialog_token_amount),
            sep='\n'
        ),
        Row(
            Cancel(Const(msg.wallet_dialog_cancel_transfer), on_click=cancel_handler),
            Button(Const(msg.wallet_dialog_confirm_transfer), id='confirm', on_click=confirm_transaction_handler)
        ),
        getter=get_data,
        state=TransferStates.finish
    )
)
