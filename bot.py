import asyncio

from src.common import bot, dp
from src.bot.handlers import include_routers


async def main():
    include_routers(dp)

    await dp.start_polling(bot, skip_update=True)


if __name__ == '__main__':
    asyncio.run(main())
