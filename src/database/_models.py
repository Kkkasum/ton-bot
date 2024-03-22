from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String


Base = declarative_base()


class Jetton(Base):
    __tablename__ = 'jettons'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(16), unique=True)
    master_address = Mapped[str] = mapped_column(String(66), unique=True)


class App(Base):
    __tablename__ = 'apps'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    url: Mapped[str]
    tg_links: Mapped[str]


# Apps
# name
# description
# platforms
# tg links
# url


# Contract Templates
# name
# description
# github code url
# contract standard
# ton docs


# Jetton
# name
# jetton_master_address
