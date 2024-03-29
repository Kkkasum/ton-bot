import asyncio

from aiogram import Router, F, types

from aiogram_dialog import DialogManager, StartMode

from pytonconnect.exceptions import FetchWalletsError

from pytoniq_core import Address, AddressError

import qrcode

from src.services.ton import Connector
from src.utils import messages as msg
from src.utils.formatters import format_connection
from src.bot.dialogs import include_transfer_dialog, TransferStates
from src.bot.keyboards import (
    wallets_kb,
    wallet_try_again_kb,
    wallet_actions_kb,
    return_menu_kb,
    MenuCallbackFactory,
    WalletCallbackFactory,
    WalletActionCallbackFactory
)


router = Router()
include_transfer_dialog(router)


@router.callback_query(MenuCallbackFactory.filter(F.page == 'wallet'))
async def wallet_menu(callback: types.CallbackQuery, **_):
    await callback.message.delete()

    connector = Connector(callback.from_user.id)

    is_connected = await connector.restore_connection()
    if is_connected:
        await callback.message.answer(text=msg.wallet_connected)
        await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())
        return

    try:
        wallets = [
            wallet['name']
            for wallet in connector.get_wallets()
        ]
    except FetchWalletsError:
        await connector.disconnect()
        wallets_list = await connector.connect(connector.get_wallets())
        wallets = [
            wallet['name']
            for wallet in wallets_list
        ]

    await callback.message.answer(text=msg.wallet, reply_markup=wallets_kb(wallets))


@router.callback_query(WalletCallbackFactory.filter())
async def wallet_callback(callback: types.CallbackQuery, callback_data: WalletCallbackFactory):
    await callback.message.delete()

    connector = Connector(callback.from_user.id)
    while True:
        try:
            url = await connector.connect(connector.get_wallets()[callback_data.index])
        except FetchWalletsError:
            await connector.disconnect()
        else:
            break

    qrcode.make(url).save(f'images/{callback.from_user.id}.png')

    qr = types.FSInputFile(f'images/{callback.from_user.id}.png')
    m = format_connection(url)

    connect_msg = await callback.message.answer_photo(photo=qr, caption=m)

    address = None
    for i in range(120):
        await asyncio.sleep(1)
        if connector.connected:
            try:
                address = Address(connector.account.address)
            except AddressError:
                break
            else:
                break

    await connect_msg.delete()

    if not address:
        await callback.message.answer(text=msg.wallet_conn_expired, reply_markup=wallet_try_again_kb())
        return

    await callback.message.answer(text=msg.wallet_conn_succeed)
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


@router.callback_query(WalletActionCallbackFactory.filter(F.action == 'transfer'))
async def wallet_transfer(_, dialog_manager: DialogManager):
    await dialog_manager.start(state=TransferStates.address, mode=StartMode.RESET_STACK)


@router.callback_query(WalletActionCallbackFactory.filter(F.action == 'disconnect'))
async def wallet_disconnect(callback: types.CallbackQuery, **_):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()
    await connector.disconnect()

    await callback.message.delete()
    await callback.message.answer(text=msg.wallet_disconnect, reply_markup=return_menu_kb())
