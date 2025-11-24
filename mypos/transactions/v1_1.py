from typing import Optional, List
from ...schemas import MultipleTransactionDetailsResponse, AccountListResponse

class TransactionsV1_1:
    def __init__(self, client):
        self.client = client

    def get_multiple_details(self, payment_references: List[str]) -> MultipleTransactionDetailsResponse:
        """
        Get details for multiple transactions from MyPOS API (v1.1).
        """
        if len(payment_references) > 5:
            raise ValueError("Maximum 5 payment references allowed")

        response_data = self.client.request(
            "GET", 
            "/v1.1/transactions/details", 
            params={"references": ",".join(payment_references)}
        )
        return MultipleTransactionDetailsResponse(**response_data)

    def list_accounts(
        self, 
        page: Optional[int] = 1,
        size: Optional[int] = 20
    ) -> AccountListResponse:
        """
        Get accounts from MyPOS API (v1.1).
        """
        response_data = self.client.request(
            "GET", 
            "/v1.1/accounts", 
            params={"page": page, "size": size}
        )
        return AccountListResponse(**response_data)
