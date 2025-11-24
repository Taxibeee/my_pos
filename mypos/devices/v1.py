from typing import Optional
from datetime import datetime
from ...schemas import DeviceListResponse, DeviceTransactionListResponse, DeviceDetail

class DevicesV1:
    def __init__(self, client):
        self.client = client
        # Devices API uses a different base URL structure usually, but based on previous code
        # we need to replace 'transactions' with 'devices' in the base URL.
        # We'll handle this by passing the modified base URL to the request method.
        self.base_url = client.api_base_url.replace('transactions', 'devices')

    def list(
        self, 
        size: Optional[int] = 20,
        terminal_id: Optional[str] = None,
        serial_number: Optional[str] = None,
        model: Optional[str] = None
    ) -> DeviceListResponse:
        """
        Get devices from MyPOS API (v1).
        """
        body = {}
        if terminal_id:
            body["terminal_id"] = terminal_id
        if serial_number:
            body["serial_number"] = serial_number
        if model:
            body["model"] = model

        response_data = self.client.request(
            "GET", 
            "/v1/devices", 
            params={"size": size}, 
            json=body,
            base_url=self.base_url
        )
        return DeviceListResponse(**response_data)

    def list_transactions(
        self, 
        terminal_id: str,
        size: Optional[int] = 20,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        from_amount: Optional[float] = None,
        to_amount: Optional[float] = None,
        rrn: Optional[str] = None,
        stan: Optional[str] = None,
        terminal_name: Optional[str] = None,
        reference_number: Optional[str] = None
    ) -> DeviceTransactionListResponse:
        """
        Get device transactions from MyPOS API (v1).
        """
        body = {}
        if from_date:
            body["from_date"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            body["to_date"] = to_date.strftime("%Y-%m-%d")
        if from_amount is not None:
            body["from_amount"] = from_amount
        if to_amount is not None:
            body["to_amount"] = to_amount
        if rrn:
            body["rrn"] = rrn
        if stan:
            body["stan"] = stan
        if terminal_name:
            body["terminal_name"] = terminal_name
        if reference_number:
            body["reference_number"] = reference_number

        response_data = self.client.request(
            "GET", 
            f"/v1/devices/{terminal_id}/transactions", 
            params={"size": size}, 
            json=body,
            base_url=self.base_url
        )
        return DeviceTransactionListResponse(**response_data)

    def get_details(self, terminal_id: str) -> DeviceDetail:
        """
        Get device details from MyPOS API (v1).
        """
        response_data = self.client.request(
            "GET", 
            f"/v1/devices/{terminal_id}",
            base_url=self.base_url
        )
        return DeviceDetail(**response_data)
