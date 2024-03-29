from datetime import date

from pydantic import BaseModel, ConfigDict

from pytoniq_core import Address


class CollectionDaySales(BaseModel):
    put_up_for_sale_count: int
    cancel_sale_count: int
    transfer_count: int
    mint_count: int
    put_up_for_auction_count: int
    cancel_auction_count: int
    burn_count: int
    date: date
    volume: float
    avg_price: float


class CollectionSalesHistory(BaseModel):
    sales: list[CollectionDaySales]


class CollectionStats(BaseModel):
    holders_count: int
    floor_price: float
    items_count: int
    total_volume: int

    @property
    def volume(self) -> float:
        return self.total_volume / 1e9


class Collection(BaseModel):
    name: str
    address: Address

    model_config = ConfigDict(arbitrary_types_allowed=True)


class NftItem(BaseModel):
    name: str
    collection: Collection | None = None
    address: Address
    owner: Address | None = None
    img: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    @property
    def owner_address(self) -> str | None:
        return self.owner.to_str() if self.owner else None


class NftCollection(BaseModel):
    name: str
    address: Address
    owner: Address
    description: str
    stats: CollectionStats
    social_links: list[str] | None
    img: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def socials(self) -> str | None:
        return '\n' + '\n'.join(self.social_links) if self.social_links else None


class SelectNftItem(BaseModel):
    index: int
    name: str
    address: str
    img: str

    def __getitem__(self, key):
        return list(self.__dict__.values())[key]
