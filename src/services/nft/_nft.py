from pytoniq_core import Address

from ._models import Collection, NftItem, NftCollection
from ._getgems import gg
from src.common import TonAPI


class Nft(TonAPI):
    def __init__(self):
        super().__init__()
        self.nft = self.tonapi.nft

    async def get_nft_collection(self, collection_addr: Address) -> NftCollection:
        collection = await self.nft.get_collection_by_collection_address(
            account_id=collection_addr.to_str(is_user_friendly=False)
        )
        if not collection.owner:
            owner = collection_addr
        else:
            owner = Address(collection.owner.address.to_raw())

        stats = await gg.get_nft_collection_stats(collection_addr)

        return NftCollection(
            name=collection.metadata['name'],
            address=collection_addr,
            owner=owner,
            description=collection.metadata['description'],
            img=collection.metadata['image'],
            stats=stats,
            social_links=collection.metadata.get('social_links', None)
        )

    async def get_nft_item(self, nft_addr: Address) -> NftItem:
        nft_item = await self.nft.get_item_by_address(
            account_id=nft_addr.to_str(is_user_friendly=False)
        )

        owner = Address(nft_item.owner.address.to_raw()) if nft_item.owner else None

        return NftItem(
            name=nft_item.metadata['name'],
            address=nft_addr,
            owner=owner,
            collection=Collection(name=nft_item.collection.name, address=Address(nft_item.collection.address.to_raw())),
            img=nft_item.metadata['image']
        )


nft_tonapi = Nft()
