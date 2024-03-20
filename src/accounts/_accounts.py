from pytoniq_core import Address

from src.common import TonAPI
from src.nft import NftItem


class Accounts(TonAPI):
    def __init__(self):
        super().__init__()
        self.accounts = self.tonapi.accounts

    async def get_all_nft_items(self, wallet_address: str) -> list[NftItem]:
        nft_items = await self.accounts.get_all_nfts(
            account_id=wallet_address
        )

        return [
            NftItem(
                name=nft_item.metadata['name'],
                address=Address(nft_item.address.to_raw()),
                img=nft_item.metadata['image']
            )
            for nft_item in nft_items.nft_items
        ]


accounts_tonapi = Accounts()
