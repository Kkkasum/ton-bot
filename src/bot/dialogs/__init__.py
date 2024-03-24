from aiogram import Router
from aiogram.filters import ExceptionTypeFilter

from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from .jetton import jetton_dialog, JettonStates
from .wallet import transfer_dialog, TransferStates
from ._exceptions import on_unknown_intent, on_unknown_state


def include_dialog(router: Router):
    router.include_router(transfer_dialog)

    router.error.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    router.error.register(on_unknown_state, ExceptionTypeFilter(UnknownState))

    setup_dialogs(router)
