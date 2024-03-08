from aiogram import Dispatcher

from ._start import router as start_router
from ._token import router as token_router
from ._nft import router as nft_router
from ._app import router as app_router


def include_routers(dp: Dispatcher):
    dp.include_routers(
        start_router,
        token_router,
        nft_router,
        app_router
    )
