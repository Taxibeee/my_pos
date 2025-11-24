from typing import Optional, List
from datetime import datetime
from ...schemas import TransactionType, TransactionListResponse, TransactionDetailsResponse

class TransactionsV1:
    def __init__(self, client):
        self.client = client

    def list(
        self, 
        size: Optional[int] = 20,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        transaction_types: Optional[List[TransactionType]] = None,
        sign: Optional[str] = None,
        last_transaction_id: Optional[str] = None
    ) -> TransactionListResponse:
        """
        Get transactions from MyPOS API (v1).
        """
        body = {}
        if from_date:
            body["from_date"] = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if to_date:
            body["to_date"] = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if transaction_types:
            body["transaction_types"] = ",".join([t.value for t in transaction_types])
        if sign:
            body["sign"] = sign
        if last_transaction_id:
            body["last_transaction_id"] = last_transaction_id

        response_data = self.client.request(
            "GET", 
            "/v1/transactions", 
            params={"size": size}, 
            json=body
        )
        return TransactionListResponse(**response_data)

    def get_details(self, payment_reference: str) -> TransactionDetailsResponse:
        """
        Get transaction details from MyPOS API (v1).
        """
        response_data = self.client.request("GET", f"/v1/transactions/{payment_reference}")
        return TransactionDetailsResponse(**response_data)
