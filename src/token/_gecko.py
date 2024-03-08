import aiohttp


class GeckoTerminal:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def get_token_pools_price(self, token_addr: str) -> list[dict] | None:
        url = self.api_url + f'/networks/ton/tokens/{token_addr}/pools'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

        return res['data']

    async def get_dexes_token_price(self, dedust_pool: str, stonfi_pool: str) -> list[dict] | None:
        url = self.api_url + f'/networks/ton/pools/multi/{dedust_pool},{stonfi_pool}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

        return res['data']


gecko_terminal = GeckoTerminal(api_url='https://api.geckoterminal.com/api/v2')
