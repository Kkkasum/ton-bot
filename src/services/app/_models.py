from pydantic import BaseModel

from src.database import AppCategory


class App(BaseModel):
    name: str
    category: AppCategory
    description: str | None
    url: str | None
    tg_links: str | None
    img: str | None
