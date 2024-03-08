from pytoniq_core import Address

from ._models import Collection, NftItem, NftCollection
from ._getgems import gg
from src.common import TonAPI


class Nft(TonAPI):
    def __init__(self):
        super().__init__()
        self.nft = self.tonapi.nft

    async def get_nft_collection(self, collection_addr: Address) -> NftCollection:
        res_collection = await self.nft.get_collection_by_collection_address(
            account_id=collection_addr.to_str(is_user_friendly=False)
        )
        if not res_collection.owner:
            owner = collection_addr
        else:
            owner = Address(res_collection.owner.address.to_raw())

        stats = await gg.get_nft_collection_stats(collection_addr)

        return NftCollection(
            name=res_collection.metadata['name'],
            address=collection_addr,
            owner=owner,
            description=res_collection.metadata['description'],
            img=res_collection.metadata['image'],
            stats=stats,
            social_links=res_collection.metadata.get('social_links', None)
        )

    async def get_nft_item(self, nft_addr: Address) -> NftItem:
        res_nft_item = await self.nft.get_item_by_address(
            account_id=nft_addr.to_str(is_user_friendly=False)
        )

        if not res_nft_item.owner:
            owner = None
        else:
            owner = Address(res_nft_item.owner.address.to_raw())

        return NftItem(
            name=res_nft_item.metadata['name'],
            address=nft_addr,
            owner=owner,
            collection=Collection(name=res_nft_item.collection.name, address=Address(res_nft_item.collection.address.to_raw())),
            img=res_nft_item.metadata['image']
        )


nft_tonapi = Nft()
