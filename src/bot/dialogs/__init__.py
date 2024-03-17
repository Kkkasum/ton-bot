from aiogram import Router
from aiogram.filters import ExceptionTypeFilter

from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from .wallet import transfer_dialog, TransferStates
from ._exceptions import on_unknown_intent


def include_dialog(router: Router):
    router.include_router(transfer_dialog)

    router.error.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))

    setup_dialogs(router)
