import asyncio

from aiogram_dialog import setup_dialogs

from src.common import bot, dp
from src.bot import include_routers
from src.services.app import app_service


async def main():
    include_routers(dp)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
