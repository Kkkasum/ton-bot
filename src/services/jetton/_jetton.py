from pytoniq_core import Address

from src.common import TonAPI

from ._models import Token, DEX, JettonPool, DEXPools
from ._gecko import gecko_terminal, GeckoTerminal


class JettonService(TonAPI):
    def __init__(self, gt: GeckoTerminal):
        super().__init__()
        self.jetton = self.tonapi.jettons
        self.gt = gt

    async def get_jetton_info(self, jetton_addr: Address) -> Token:
        jetton_info = await self.jetton.get_info(
            account_id=jetton_addr.to_str(is_user_friendly=False)
        )

        return Token(
            name=jetton_info.metadata.name,
            address=jetton_addr,
            symbol=jetton_info.metadata.symbol,
            total_supply=jetton_info.total_supply,
            holders_count=jetton_info.holders_count,
            img=jetton_info.metadata.image
        )

    async def get_dexes(self) -> list[DEX]:
        dexes = await self.gt.get_dexes()

        return [
            DEX(
                id=dex['id'],
                name=dex['attributes']['name']
            )
            for dex in dexes
        ]

    async def get_dex_pools(self, dex: str, jetton_addr: Address) -> DEXPools:
        jetton_pools = await self.gt.get_token_pools(jetton_addr.to_str())
        dex_pools = DEXPools(
            pools=[
                JettonPool(
                    name=pool['attributes']['name'],
                    created_at=pool['attributes']['pool_created_at'],
                    price_native=pool['attributes']['base_token_price_native_currency'],
                    price_usd=pool['attributes']['base_token_price_usd']
                )
                for pool in jetton_pools
                if pool['relationships']['dex']['data']['id'] == dex
            ]
        )

        return dex_pools


jettons = JettonService(gt=gecko_terminal)
