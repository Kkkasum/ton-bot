from time import time
from base64 import urlsafe_b64encode

from pytoniq_core import Cell, begin_cell

from ._transaction import Transaction, TransactionMessage


class TONTransferTransaction(Transaction):
    def __init__(
        self,
        address: str,
        amount: int | float,
        comment: str = ''
    ):
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0, 32)  # op code for comment message
            .store_string(comment)
            .end_cell()
            .to_boc()
        )

        super().__init__(
            valid_until=int(time() + 360),
            messages=[
                TransactionMessage(
                    address=address,
                    amount=amount * 1e9,
                    payload=payload
                )
            ]
        )


class JettonTransferTransaction(Transaction):
    def __init__(
        self,
        jetton_wallet_address: str,
        recipient_address: str,
        comment: str,
        jetton_amount: int,
        jetton_decimal: int = 9,
        query_id: int = 0,
        response_address: str | None = None,
        transfer_fee: int | float = 0.05,
        custom_payload: Cell = Cell.empty(),
        forward_amount: int | float = 0.01
    ):
        forward_payload = (begin_cell()
                           .store_uint(0, 32)
                           .store_snake_string(comment)
                           .end_cell())

        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0xf8a7ea5, 32)  # op code for jetton transfer message
            .store_uint(query_id, 64)
            .store_coins(int(jetton_amount * 10 ** jetton_decimal))
            .store_address(recipient_address)  # destination address
            .store_address(response_address)  # address send excess to
            .store_maybe_ref(custom_payload)
            .store_coins(int(forward_amount * 1e9))
            .store_maybe_ref(forward_payload)
            .end_cell()
            .to_boc()
        ).decode()

        super().__init__(
            valid_until=int(time() + 360),
            messages=[
                TransactionMessage(
                    address=jetton_wallet_address,
                    payload=payload,
                    amount=str(int(transfer_fee * 1e9))
                )
            ]
        )


class NFTTransferTransaction(Transaction):
    def __init__(
        self,
        nft_address: str,
        recipient_address: str,
        query_id: int = 0,
        response_address: str | None = None,
        transfer_fee: int | float = 0.07,
        custom_payload: Cell = Cell.empty(),
        forward_payload: Cell = Cell.empty(),
        forward_amount: int | float = 0.01
    ):
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0x5fcc3d14, 32)
            .store_uint(query_id, 64)
            .store_address(recipient_address)
            .store_address(response_address)
            .store_maybe_ref(custom_payload)
            .store_coins(int(forward_amount * 1e9))
            .store_maybe_ref(forward_payload)
            .end_cell()
            .to_boc()
        ).decode()

        super().__init__(
            valid_until=int(time() + 360),
            messages=[
                TransactionMessage(
                    address=nft_address,
                    payload=payload,
                    amount=str(int(transfer_fee * 1e9))
                )
            ]
        )
