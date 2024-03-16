import asyncio

from aiogram import Router, F, types

from pytonconnect.exceptions import FetchWalletsError

from pytoniq_core import Address, AddressError

import qrcode

from src.ton import get_connector
from src.utils import messages as msg
from src.utils.formatters import format_connection
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


@router.callback_query(MenuCallbackFactory.filter(F.page == 'wallet'))
async def wallet_menu(callback: types.CallbackQuery, callback_data: MenuCallbackFactory):
    connector = get_connector(callback.from_user.id)

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

    await callback.message.edit_text(text=msg.wallet, reply_markup=wallets_kb(wallets))


@router.callback_query(WalletCallbackFactory.filter())
async def wallet_callback(callback: types.CallbackQuery, callback_data: WalletCallbackFactory):
    connector = get_connector(callback.from_user.id)

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

    await callback.message.delete()
    connect_msg = await callback.message.answer_photo(photo=qr, caption=m)

    address = None
    for i in range(120):
        await asyncio.sleep(1)
        if connector.connected:
            try:
                address = Address(connector.account.address)
            except AddressError:
                break

    await connect_msg.delete()

    if not address:
        await callback.message.answer(text=msg.wallet_conn_expired, reply_markup=wallet_try_again_kb())
        return

    await callback.message.answer(text=msg.wallet_conn_succeed)
    await callback.message.answer(text=msg.menu, reply_markup=wallet_actions_kb())


@router.callback_query(WalletActionCallbackFactory.filter(F.action == 'disconnect'))
async def wallet_action_callback(callback: types.CallbackQuery, callback_data: WalletActionCallbackFactory):
    connector = get_connector(callback.from_user.id)
    await connector.restore_connection()
    await connector.disconnect()

    await callback.message.edit_text(text=msg.wallet_disconnect, reply_markup=return_menu_kb())
