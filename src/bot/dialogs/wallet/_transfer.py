from aiogram import Router, types

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Row, Cancel

from pytoniq_core import Address, AddressError

from pytonconnect.exceptions import UserRejectsError, WalletNotConnectedError

from ._states import TransferStates
from src.utils import messages as msg
from src.bot.keyboards import wallet_actions_kb, return_menu_kb
from src.ton import Connector, TONTransferTransaction, JettonTransferTransaction, Provider


router = Router()


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'address': dialog_manager.dialog_data.get('address', None),
        'token': dialog_manager.dialog_data.get('token', None),
        'amount': dialog_manager.dialog_data.get('amount', None),
        'comment': dialog_manager.dialog_data.get('comment', None)
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

    await dm.switch_to(state=TransferStates.amount)


async def amount_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer(text=msg.wallet_amount_error)
        await dm.done()
        return

    dm.dialog_data['amount'] = amount

    await dm.next()


async def comment_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    dm.dialog_data['comment'] = message.text

    await dm.next()


async def empty_comment_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    dm.dialog_data['comment'] = 'нет'

    await dm.next()


async def cancel_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


async def confirm_transaction_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()

    comment = dm.dialog_data['comment']
    if comment == 'нет':
        comment = ''

    if dm.dialog_data['token'] == 'TON':
        transfer_transaction = TONTransferTransaction(
            address=dm.dialog_data['address'],
            amount=dm.dialog_data['amount'],
            comment=comment
        )
    else:
        provider = Provider()
        jetton_wallet_address = await provider.get_jetton_wallet_address(
            jetton_master_address='EQD26zcd6Cqpz7WyLKVH8x_cD6D7tBrom6hKcycv8L8hV0GP',
            address=dm.dialog_data['address']
        )

        transfer_transaction = JettonTransferTransaction(
            jetton_wallet_address=jetton_wallet_address.to_str(),
            recipient_address=dm.dialog_data['address'],
            jetton_amount=dm.dialog_data['amount'],
            comment=comment
        )

    approve_msg = await callback.message.answer(text=msg.wallet_dialog_approve_transfer)

    try:
        await connector.send_transaction(transaction=transfer_transaction.model_dump())
    except UserRejectsError:
        await approve_msg.delete()
        await callback.message.answer(text=msg.wallet_dialog_rejected_transfer)
    except WalletNotConnectedError:
        await callback.message.answer(text=msg.wallet_not_connected)
        await callback.message.answer(text=msg.menu, reply_markup=return_menu_kb())


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
        Format(msg.wallet_dialog_amount_input),
        MessageInput(amount_handler, content_types=[types.ContentType.TEXT]),
        getter=get_data,
        state=TransferStates.amount
    ),
    Window(
        Const(msg.wallet_dialog_comment_input),
        MessageInput(comment_handler, content_types=[types.ContentType.TEXT]),
        Button(Const('Без комментария'), id='empty_comment', on_click=empty_comment_handler),
        state=TransferStates.comment
    ),
    Window(
        Multi(
            Format(msg.wallet_dialog_address),
            Format(msg.wallet_dialog_amount),
            Format(msg.wallet_dialog_comment),
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
