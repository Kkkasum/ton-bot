from aiogram import Dispatcher

from ._menu import router as menu_router
from ._wallet import router as wallet_router
from ._jetton import router as jetton_router
from ._nft import router as nft_router
from ._app import router as app_router


def include_routers(dp: Dispatcher):
    dp.include_routers(
        menu_router,
        wallet_router,
        jetton_router,
        nft_router,
        app_router
    )
