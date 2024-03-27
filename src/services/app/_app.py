from ._models import App
from src.repos import AppRepo


class AppService:
    def __init__(self):
        super().__init__()
        self.repo = AppRepo()

    @property
    def categories(self) -> list[str]:
        return self.repo.get_categories()

    async def get_apps_by_category(self, category: str) -> list[tuple[int, str]]:
        apps = await self.repo.get_apps_by_category(category)

        return [
            (index, *app)
            for index, app in enumerate(apps)
        ]

    async def get_app(self, app_name: str):
        app = await self.repo.get_app(app_name)

        return App(
            name=app_name,
            category=app[0],
            description=app[1],
            url=app[2],
            tg_links=app[3],
            img=app[4]
        )


app_service = AppService()
