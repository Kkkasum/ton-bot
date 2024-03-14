from datetime import datetime

from pydantic import BaseModel, ConfigDict

from pytoniq_core import Address


class Token(BaseModel):
    name: str
    symbol: str
    address: Address
    total_supply: float | None
    holders_count: int
    img: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def supply(self) -> float:
        return self.total_supply / 10 ** 9


# class Tokens(BaseModel):
#     SCALE: Token = Token(address=Address(''))
#     DFC: Token = Token(address=Address(''))
#     RAFF: Token = Token(address=Address(''))
#     JVT: Token = Token(address=Address('EQC8FoZMlBcZhZ6Pr9sHGyHzkFv9y2B5X9tN61RvucLRzFZz'))


class DEX(BaseModel):
    id: str
    name: str


class JettonPool(BaseModel):
    name: str
    created_at: datetime
    price_native: float
    price_usd: float

    @property
    def creation_datetime(self) -> str:
        return self.created_at.strftime('%d.%m.%Y %H:%M:%S')

    @property
    def main_jetton(self) -> str:
        return self.name.split()[0]


class DEXPools(BaseModel):
    pools: list[JettonPool]
