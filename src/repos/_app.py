from sqlalchemy import select

from src.database import Database, App


class AppRepo(Database):
    def __init__(self):
        super().__init__()
