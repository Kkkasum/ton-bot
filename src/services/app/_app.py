from src.repos import AppRepo


class AppService:
    def __init__(self):
        super().__init__()
        self.repo = AppRepo()


app_service = AppService()
