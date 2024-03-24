import operator

from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import Dialog, DialogManager, Window, ShowMode
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    SwitchTo,
    Back,
    Cancel,
    Row,
    Column,
    Select,
    ScrollingGroup
)

from pytoniq_core import Address, AddressError

from pytonconnect.exceptions import UserRejectsError, WalletNotConnectedError

from ._states import TransferStates
from src.utils import messages as msg
from src.utils.formatters import format_dialog_nft_item
from src.bot.keyboards import wallet_actions_kb, wallet_return_kb
from src.ton import Connector, TONTransferTransaction, JettonTransferTransaction, NFTTransferTransaction, Provider
from src.services.accounts import accounts_service
from src.services.nft import SelectedNftItem


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'address': dialog_manager.dialog_data.get('address', None),
        'token': dialog_manager.dialog_data.get('token', None),
        'amount': dialog_manager.dialog_data.get('amount', None),
        'nft_items': dialog_manager.dialog_data.get('nft_items', None),
        'comment': dialog_manager.dialog_data.get('comment', None)
    }


async def address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    await message.delete()

    try:
        address = Address(message.text)
    except (AddressError, ValueError):
        await message.answer(text=msg.wallet_address_error)
        await message.answer(text=msg.menu, reply_markup=wallet_actions_kb())

        await dm.done()
        return

    dm.dialog_data['address'] = address.to_str(is_user_friendly=True)

    await dm.switch_to(state=TransferStates.token, show_mode=ShowMode.DELETE_AND_SEND)


async def token_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()

    dm.dialog_data['token'] = button.text.text

    await dm.switch_to(state=TransferStates.amount, show_mode=ShowMode.DELETE_AND_SEND)


async def amount_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    await message.delete()

    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer(text=msg.wallet_amount_error)
        await dm.done()
        return

    dm.dialog_data['amount'] = amount

    await dm.switch_to(state=TransferStates.comment, show_mode=ShowMode.DELETE_AND_SEND)


async def nft_address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    await message.delete()

    try:
        Address(message.text)
    except AddressError:
        await message.answer(text=msg.nft_contract_error, reply_markup=wallet_return_kb())
        await dm.done()

    dm.dialog_data['nft_address'] = message.text

    await dm.switch_to(state=TransferStates.comment, show_mode=ShowMode.DELETE_AND_SEND)


async def nft_items_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()

    nft_items = await accounts_service.get_all_nft_items(wallet_address=connector.account.address)

    dm.dialog_data['nft_items'] = [
        SelectedNftItem(
            index=index,
            name=nft_item.name,
            address=nft_item.address.to_str(),
            img=nft_item.img
        )
        for index, nft_item in enumerate(nft_items)
    ]

    await dm.switch_to(state=TransferStates.nft_items, show_mode=ShowMode.DELETE_AND_SEND)


async def on_nft_item_selected(callback: types.CallbackQuery, s_btn: Select, dm: DialogManager, item_id: str):
    selected_nft_item = dm.dialog_data['nft_items'][int(item_id)]

    dm.dialog_data['selected_nft_address'] = selected_nft_item.address

    m = format_dialog_nft_item(selected_nft_item)
    img = types.URLInputFile(selected_nft_item.img)

    try:
        await callback.message.delete()
        await callback.message.answer_photo(photo=img, caption=m)
    except (AssertionError, TelegramBadRequest):
        await callback.message.answer(text=m)

    await dm.switch_to(state=TransferStates.comment)


async def nft_item_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.answer(text=msg.wallet_dialog_nft_item)

    await dm.next()


async def comment_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    await message.delete()

    dm.dialog_data['comment'] = message.text

    if dm.dialog_data.get('amount', None):
        await dm.switch_to(state=TransferStates.finish, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dm.switch_to(state=TransferStates.nft_finish, show_mode=ShowMode.DELETE_AND_SEND)


async def empty_comment_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()

    dm.dialog_data['comment'] = 'нет'

    if dm.dialog_data.get('amount', None):
        await dm.switch_to(state=TransferStates.finish, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dm.switch_to(state=TransferStates.nft_finish, show_mode=ShowMode.DELETE_AND_SEND)


async def cancel_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await callback.message.delete()
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


async def confirm_transaction_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()

    comment = dm.dialog_data['comment']
    if comment == 'нет':
        comment = ''

    if dm.dialog_data.get('selected_nft_address', None):
        transfer_transaction = NFTTransferTransaction(
            nft_address=dm.dialog_data['selected_nft_address'],
            recipient_address=dm.dialog_data['address'],
        )
    elif dm.dialog_data.get('token', None) == 'TON':
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
        await callback.message.answer(text=msg.wallet_dialog_rejected_transfer)
    except WalletNotConnectedError:
        await callback.message.answer(text=msg.wallet_not_connected)
    finally:
        await approve_msg.delete()
        await callback.message.answer(text=msg.menu, reply_markup=wallet_return_kb())

    await dm.done()


dialog = Dialog(
    Window(
        Const(msg.wallet_dialog_address_input),
        MessageInput(address_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        state=TransferStates.address
    ),
    Window(
        Const(msg.wallet_dialog_token),
        Row(
            Button(Const('TON'), id='ton', on_click=token_handler),
            SwitchTo(Const('Jetton'), id='jetton', state=TransferStates.jetton),
            SwitchTo(Const('NFT'), id='nft', state=TransferStates.nft),
        ),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад')),
        state=TransferStates.token
    ),
    Window(
        Const(msg.wallet_dialog_jetton),
        Column(
            Button(Const('DFC'), id='dfc', on_click=token_handler),
            Button(Const('TONNEL'), id='tonnel', on_click=token_handler),
        ),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад')),
        state=TransferStates.jetton
    ),
    Window(
        Format(msg.wallet_dialog_amount_input),
        MessageInput(amount_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад')),
        getter=get_data,
        state=TransferStates.amount
    ),
    Window(
        Const(msg.wallet_dialog_nft_input),
        SwitchTo(Const('По адресу NFT'), id='nft_address', state=TransferStates.nft_address),
        Button(Const('Выбрать из доступных'), id='available_nft_items', on_click=nft_items_handler),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад')),
        state=TransferStates.nft
    ),
    Window(
        Const(msg.wallet_dialog_nft_address_input),
        MessageInput(nft_address_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        state=TransferStates.nft_address
    ),
    Window(
        Const(msg.wallet_dialog_nft_items),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='s_nft_items',
                item_id_getter=operator.itemgetter(0),
                items='nft_items',
                on_click=on_nft_item_selected
            ),
            id='nft_items',
            width=1,
            height=5
        ),
        getter=get_data,
        state=TransferStates.nft_items
    ),
    Window(
        Const(msg.wallet_dialog_comment_input),
        MessageInput(comment_handler, content_types=[types.ContentType.TEXT]),
        Button(Const('Без комментария'), id='empty_comment', on_click=empty_comment_handler),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
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
    ),
    Window(
        Multi(
            Format(msg.wallet_dialog_address),
            Format(msg.wallet_dialog_comment),
            sep='\n'
        ),
        Row(
            Cancel(Const(msg.wallet_dialog_cancel_transfer), on_click=cancel_handler),
            Button(Const(msg.wallet_dialog_confirm_transfer), id='confirm', on_click=confirm_transaction_handler)
        ),
        getter=get_data,
        state=TransferStates.nft_finish
    )
)
