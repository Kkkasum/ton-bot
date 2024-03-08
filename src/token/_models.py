from pydantic import BaseModel, ConfigDict

from pytoniq_core import Address


class Token(BaseModel):
    name: str
    address: Address
    symbol: str
    total_supply: float | None

    model_config = ConfigDict(arbitrary_types_allowed=True)


# class Tokens(BaseModel):
#     SCALE: Token = Token(address=Address(''))
#     DFC: Token = Token(address=Address(''))
#     RAFF: Token = Token(address=Address(''))
#     JVT: Token = Token(address=Address('EQC8FoZMlBcZhZ6Pr9sHGyHzkFv9y2B5X9tN61RvucLRzFZz'))


class TokenPool(BaseModel):
    dex: str
    pool_name: str
    price_native: float
    price_usd: float
