from sqlalchemy import select

from src.database import Database, Jetton


class JettonRepo(Database):
    def __init__(self):
        super().__init__()

    async def get_jettons(self):
        async with self.session_maker() as session:
            query = select(Jetton.name)
            res = await session.execute(query)

        return res.fetchall()

    async def get_jetton_master_address(self, symbol: str) -> str:
        async with self.session_maker() as session:
            query = select(Jetton.master_address) \
                .where(Jetton.symbol == symbol)
            res = await session.execute(query)

        return res.fetchone()
