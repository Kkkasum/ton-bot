from aiogram import Router
from aiogram.filters import ExceptionTypeFilter

from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from .jetton import (
    jetton_dialog,
    on_unknown_intent as jetton_on_unknown_intent,
    on_unknown_state as jetton_on_unknown_state
)
from .wallet import (
    transfer_dialog,
    on_unknown_intent as wallet_on_unknown_intent,
    on_unknown_state as wallet_on_unknown_state
)


# можно поменять, чтобы в файлах с диалогом был свой роутер, потом этот роутер включать в роутер хэндлера
def include_jetton_dialog(router: Router):
    router.include_router(jetton_dialog)

    router.error.register(jetton_on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    router.error.register(jetton_on_unknown_state, ExceptionTypeFilter(UnknownState))


def include_transfer_dialog(router: Router):
    router.include_router(transfer_dialog)

    router.error.register(wallet_on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    router.error.register(wallet_on_unknown_state, ExceptionTypeFilter(UnknownState))
