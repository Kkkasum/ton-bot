from sqlalchemy import select

from src.database import Database, App, AppCategory


class AppRepo(Database):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_categories() -> list[str]:
        return [
            category.value
            for category in AppCategory
        ]

    async def get_apps_by_category(self, category: str) -> list[str]:
        async with self.session_maker() as session:
            query = select(App.name)\
                .where(App.category == category)
            res = await session.execute(query)

        return res.fetchall()

    async def get_app(self, app_name: str) -> list:
        async with self.session_maker() as session:
            query = select(App.category, App.description, App.url, App.tg_links, App.img)\
                .where(App.name == app_name)
            res = await session.execute(query)

        return res.fetchone()
