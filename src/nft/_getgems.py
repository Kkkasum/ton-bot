from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from pytoniq_core import Address

from ._models import CollectionStats, NftCollection, CollectionDaySales, CollectionSalesHistory


class GetGems:
    def __init__(self, url: str):
        self.transport = AIOHTTPTransport(url=url)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def get_nft_collection_stats(self, collection_addr: Address) -> CollectionStats:
        async with self.client as session:
            query = gql(
                """
                query NftCollectionStats($address: String!) {
                    alphaNftCollectionStats(address: $address) {
                        floorPrice
                        itemsCount
                        totalVolumeSold
                    }
                    nftCollectionByAddress(address: $address) {
                        approximateHoldersCount
                    }
                }
                """
            )
            params = {'address': collection_addr.to_str()}
            res = await session.execute(query, variable_values=params)

        collection_stats = res['alphaNftCollectionStats'] | res['nftCollectionByAddress']

        return CollectionStats(
            holders_count=collection_stats['approximateHoldersCount'],
            floor_price=collection_stats['floorPrice'],
            items_count=collection_stats['itemsCount'],
            total_volume=collection_stats['totalVolumeSold']
        )

    async def get_nft_collection(self, collection_addr: Address) -> NftCollection:
        async with self.client as session:
            query = gql(
                """
                query NftCollectionByAddress($address: String!) {
                    nftCollectionByAddress(address: $address) {
                        name
                        ownerAddress
                        description
                        image {
                          originalUrl
                        }
                        approximateHoldersCount
                        approximateItemsCount
                        socialLinks
                    }
                }
                """
            )
            params = {'address': collection_addr.to_str()}
            res = await session.execute(query, variable_values=params)

        nft_collection = res['nftCollectionByAddress']
        stats = await self.get_nft_collection_stats(collection_addr)

        return NftCollection(
            name=nft_collection['name'],
            address=collection_addr,
            owner=Address(nft_collection['ownerAddress']),
            description=nft_collection['description'],
            img=nft_collection['image']['originalUrl'],
            stats=stats,
            social_links=nft_collection.get('socialLinks', None)
        )

    async def get_collection_sales_history(self, collection_addr: Address, days_count: int):
        async with self.client as session:
            query = gql(
                """
                query HistoryCollectionSales($collectionAddress: String!, $daysCount: Int) {
                    historyCollectionSales(collectionAddress: $collectionAddress, daysCount: $daysCount) {
                        items {
                            putUpForSaleCount
                            cancelSaleCount
                            transferCount
                            mintCount
                            putUpForAuctionCount
                            cancelAuctionCount
                            burnCount
                            date
                            sum
                            sumAvg
                        }
                    }
                }
                """
            )
            params = {'collectionAddress': collection_addr.to_str(), 'daysCount': days_count}
            res = await session.execute(query, variable_values=params)

        collection_sales_history = res['historyCollectionSales']['items']
        collection_day_sales = [
            CollectionDaySales(
                put_up_for_sale_count=collection_day_sales['putUpForSaleCount'],
                cancel_sale_count=collection_day_sales['cancelSaleCount'],
                transfer_count=collection_day_sales['transferCount'],
                mint_count=collection_day_sales['mintCount'],
                put_up_for_auction_count=collection_day_sales['putUpForAuctionCount'],
                cancel_auction_count=collection_day_sales['cancelAuctionCount'],
                burn_count=collection_day_sales['burnCount'],
                date=collection_day_sales['date'],
                volume=collection_day_sales['sum'],
                avg_price=collection_day_sales['sumAvg'],
            )
            for collection_day_sales in collection_sales_history
        ]

        return CollectionSalesHistory(
            sales=collection_day_sales
        )


gg = GetGems(url='https://api.getgems.io/graphql')
