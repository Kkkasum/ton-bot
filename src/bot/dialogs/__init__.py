from aiogram import Router

from aiogram_dialog import setup_dialogs

from .wallet import transfer_dialog, TransferStates


def include_dialog(router: Router):
    router.include_router(transfer_dialog)

    setup_dialogs(router)
