from pytoniq_core import Address

from ._models import Token, TokenPool
from ._gecko import gecko_terminal, GeckoTerminal


class Jetton:
    def __init__(self, gt: GeckoTerminal):
        self.gt = gt

    async def get_token_base_info(self, token_addr: Address) -> Token:
        pass

    @staticmethod
    async def get_token_pools_by_contract(self, token_addr: Address) -> list[TokenPool]:
        token_pools = await self.gt.get_token_pools_price(token_addr.to_str(is_bounceable=True))

        token_data = [
            (
                TokenPool(
                    dex=pool['relationships']['dex']['data']['id'],
                    pool_name=pool['attributes']['name'],
                    price_native=pool['attributes']['base_token_price_native_currency'],
                    price_usd=pool['attributes']['base_token_price_usd']
                )
            )
            for pool in token_pools
        ]

        return token_data


jetton = Jetton(gt=gecko_terminal)
