from aiogram import Router, types

from aiogram_dialog import Dialog, DialogManager, Window, ShowMode


router = Router()


async def get_data(dialog_manager: DialogManager, **_):
    return {
        'symbol': dialog_manager.dialog_data.get('symbol', None),
        'master_address': dialog_manager.dialog_data.get('master_address', None)
    }


dialog = 'Dialog()'
