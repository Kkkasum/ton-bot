import asyncio

from aiogram import Router, F, types

from pytonconnect.exceptions import FetchWalletsError

from pytoniq_core import Address, AddressError

import qrcode

from src.bot.keyboards import wallets_kb, return_menu_kb, MenuCallbackFactory, WalletCallbackFactory
from src.ton import get_connector
from src.utils import messages as msg
from src.utils.formatters import format_connection


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

    await callback.message.answer(text=msg.wallet, reply_markup=wallets_kb(wallets))


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

    await callback.message.answer_photo(photo=qr, caption=m)

    address = None
    for i in range(5):
        await asyncio.sleep(1)
        if connector.connected:
            try:
                address = Address(connector.account.address)
            except AddressError:
                break

    if not address:
        await callback.message.edit_text(text=msg.wallet_connection_expired, reply_markup=return_menu_kb())
