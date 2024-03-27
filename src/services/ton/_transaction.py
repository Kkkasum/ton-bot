from typing import Any

from pydantic import BaseModel


class TransactionMessage(BaseModel):
    address: str
    amount: int | float
    payload: str


class Transaction(BaseModel):
    valid_until: int
    messages: list[TransactionMessage]

    def model_dump(self, **kwargs) -> dict[str, Any]:
        data = super().model_dump(**kwargs)

        return data
