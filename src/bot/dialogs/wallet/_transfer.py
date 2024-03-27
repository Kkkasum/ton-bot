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
    Select,
    ScrollingGroup
)

from pytoniq_core import Address, AddressError

from pytonconnect.exceptions import UserRejectsError, WalletNotConnectedError

from ._states import TransferStates
from src.utils import messages as msg
from src.utils.formatters import format_dialog_nft_item
from src.bot.keyboards import wallet_actions_kb, return_wallet_kb
from src.services.ton import Connector, TONTransferTransaction, JettonTransferTransaction, NFTTransferTransaction, Provider
from src.services.accounts import accounts_service
from src.services.jetton import jetton_service
from src.services.nft import SelectNftItem


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'address': dialog_manager.dialog_data.get('address', None),
        'jettons': dialog_manager.dialog_data.get('jettons', None),
        'token': dialog_manager.dialog_data.get('token', None),
        'amount': dialog_manager.dialog_data.get('amount', None),
        'comment': dialog_manager.dialog_data.get('comment', None)
    }


async def address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    await message.delete()

    try:
        address = Address(message.text)
    except (AddressError, ValueError):
        await message.answer(text=msg.wallet_dialog_address_error)
        await message.answer(text=msg.menu, reply_markup=wallet_actions_kb())

        await dm.done()
        return

    dm.dialog_data['address'] = address.to_str(is_user_friendly=True)

    await dm.switch_to(state=TransferStates.token, show_mode=ShowMode.DELETE_AND_SEND)


async def jetton_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    dm.dialog_data['jettons'] = await jetton_service.get_select_jettons()

    await dm.switch_to(state=TransferStates.jetton)


async def on_jetton_selected(callback: types.CallbackQuery, s_btn: Select, dm: DialogManager, item_id: str):
    dm.dialog_data['jetton'] = dm.dialog_data['jettons'][int(item_id)]
    dm.dialog_data['token'] = dm.dialog_data['jetton'].symbol

    await dm.switch_to(state=TransferStates.amount)


async def amount_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer(text=msg.wallet_dialog_amount_error)
        await dm.done()
        return

    dm.dialog_data['amount'] = amount

    await dm.switch_to(state=TransferStates.comment, show_mode=ShowMode.DELETE_AND_SEND)


async def nft_address_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
    try:
        Address(message.text)
    except AddressError:
        await message.answer(text=msg.nft_contract_error, reply_markup=return_wallet_kb())
        await dm.done()

    dm.dialog_data['nft_address'] = message.text

    await dm.switch_to(state=TransferStates.comment, show_mode=ShowMode.DELETE_AND_SEND)


async def nft_items_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()

    nft_items = await accounts_service.get_all_nft_items(wallet_address=connector.account.address)

    dm.dialog_data['nft_items'] = [
        SelectNftItem(
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


async def comment_handler(message: types.Message, message_input: MessageInput, dm: DialogManager):
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


async def cancel_handler(callback: types.CallbackQuery, *_):
    await callback.message.delete()
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


async def back_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    await dm.back()


async def confirm_transaction_handler(callback: types.CallbackQuery, button: Button, dm: DialogManager):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()

    comment = dm.dialog_data['comment'] if dm.dialog_data['comment'] != 'нет' else ''

    if dm.dialog_data.get('selected_nft_address', None):
        transfer_transaction = NFTTransferTransaction(
            nft_address=dm.dialog_data['selected_nft_address'],
            recipient_address=dm.dialog_data['address'],
        )
    elif dm.dialog_data.get('token', None) == 'TON':
        dm.dialog_data['token'] = 'TON'
        transfer_transaction = TONTransferTransaction(
            address=dm.dialog_data['address'],
            amount=dm.dialog_data['amount'],
            comment=comment
        )
    else:
        dm.dialog_data['token'] = dm.dialog_data['jetton'].symbol

        provider = Provider()
        jetton_wallet_address = await provider.get_jetton_wallet_address(
            jetton_master_address=dm.dialog_data['jetton'].address,
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
        await callback.message.answer(text=msg.wallet_dialog_not_connected)
    finally:
        await approve_msg.delete()
        await callback.message.answer(text=msg.menu, reply_markup=return_wallet_kb())

    await dm.done()


dialog = Dialog(
    Window(
        Const(msg.wallet_dialog_address_input),
        MessageInput(address_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        state=TransferStates.address
    ),  # input destination address
    Window(
        Const(msg.wallet_dialog_token),
        Row(
            SwitchTo(Const('TON'), id='ton', state=TransferStates.amount),
            Button(Const('Jetton'), id='jetton', on_click=jetton_handler),
            SwitchTo(Const('NFT'), id='nft', state=TransferStates.nft),
        ),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад'), on_click=back_handler),
        state=TransferStates.token
    ),  # choose token to transfer
    Window(
        Const(msg.wallet_dialog_jetton),
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
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад'), on_click=back_handler),
        getter=get_data,
        state=TransferStates.jetton
    ),  # choose jetton to transfer
    Window(
        Format(msg.wallet_dialog_amount_input),
        MessageInput(amount_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад'), on_click=back_handler),
        getter=get_data,
        state=TransferStates.amount
    ),  # input ton or jetton amount
    Window(
        Const(msg.wallet_dialog_nft_input),
        SwitchTo(Const('По адресу NFT'), id='nft_address', state=TransferStates.nft_address),
        Button(Const('Выбрать из доступных'), id='available_nft_items', on_click=nft_items_handler),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        Back(Const('◀ Назад'), on_click=back_handler),
        state=TransferStates.nft
    ),  # choose the way for nft input
    Window(
        Const(msg.wallet_dialog_nft_address_input),
        MessageInput(nft_address_handler, content_types=[types.ContentType.TEXT]),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        state=TransferStates.nft_address
    ),  # input nft address for transfer
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
    ),  # choose nft to transfer
    Window(
        Const(msg.wallet_dialog_comment_input),
        MessageInput(comment_handler, content_types=[types.ContentType.TEXT]),
        Button(Const('Без комментария'), id='empty_comment', on_click=empty_comment_handler),
        Cancel(Const('◀ Кошелек'), on_click=cancel_handler),
        state=TransferStates.comment
    ),  # input comment
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
    ),  # result for TON and jetton
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
    )  # result for NFT
)
