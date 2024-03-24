from pytoniq_core import Address

from src.common import TonAPI
from src.services.nft import NftItem


class AccountsService(TonAPI):
    def __init__(self):
        super().__init__()
        self.accounts = self.tonapi.accounts

    @staticmethod
    def validate_img_url(img_url: str) -> str:
        if 'ipfs://' in img_url:
            img_url = 'https://cloudflare-ipfs.com/ipfs/' + img_url.replace('ipfs://', '')

        return img_url

    async def get_all_nft_items(self, wallet_address: str) -> list[NftItem]:
        nft_items = await self.accounts.get_all_nfts(
            account_id=wallet_address
        )

        return [
            NftItem(
                name=nft_item.metadata['name'],
                address=Address(nft_item.address.to_raw()),
                img=self.validate_img_url(nft_item.metadata['image'])
            )
            for nft_item in nft_items.nft_items
        ]

    async def get_all_jettons(self, wallet_address: str) -> list[str]:
        jettons_balances = await self.accounts.get_jettons_balances(
            account_id=wallet_address
        )

        return [
            jetton_balance.jetton.symbol
            for jetton_balance in jettons_balances.balances
            if jetton_balance.balance != '0'
        ]


accounts_service = AccountsService()
