from typing import Optional
from ...schemas import DeviceListResponse, DeviceTransactionListResponse, DeviceDetail, ReceiptDetail

class DevicesV1_1:
    def __init__(self, client):
        self.client = client
        # Devices API uses a different base URL
        self.base_url = "https://devices-api.mypos.com"

    def list(
        self,
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        terminal_id: Optional[str] = None,
        serial_number: Optional[str] = None,
        model: Optional[str] = None
    ) -> DeviceListResponse:
        """
        List devices.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            terminal_id: Filter by terminal ID (optional)
            serial_number: Filter by serial number (optional)
            model: Filter by device model (optional)

        Returns:
            DeviceListResponse: Object containing list of devices and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        if terminal_id is not None:
            params["terminal_id"] = terminal_id
        if serial_number is not None:
            params["serial_number"] = serial_number
        if model is not None:
            params["model"] = model
        
        response_data = self.client.request(
            "GET",
            "/v1.1/devices",
            params=params,
            base_url=self.base_url
        )
        return DeviceListResponse(**response_data)

    def list_transactions(
        self,
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        from_amount: Optional[float] = None,
        to_amount: Optional[float] = None,
        rrn: Optional[str] = None,
        stan: Optional[str] = None,
        terminal_name: Optional[str] = None,
        reference_number: Optional[str] = None,
        terminal_id: Optional[str] = None
    ) -> DeviceTransactionListResponse:
        """
        List device transactions.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            from_date: Starting date in format YYYY-MM-DD (optional)
            to_date: End date in format YYYY-MM-DD (optional)
            from_amount: Minimum transaction amount (optional)
            to_amount: Maximum transaction amount (optional)
            rrn: Filter by RRN value (optional)
            stan: Filter by STAN value (optional)
            terminal_name: Filter by custom POS device name (optional)
            reference_number: Filter by reference number (optional)
            terminal_id: Filter by terminal ID (optional)

        Returns:
            DeviceTransactionListResponse: Object containing list of device transactions and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date
        if from_amount is not None:
            params["from_amount"] = from_amount
        if to_amount is not None:
            params["to_amount"] = to_amount
        if rrn is not None:
            params["rrn"] = rrn
        if stan is not None:
            params["stan"] = stan
        if terminal_name is not None:
            params["terminal_name"] = terminal_name
        if reference_number is not None:
            params["reference_number"] = reference_number
        if terminal_id is not None:
            params["terminal_id"] = terminal_id
        
        response_data = self.client.request(
            "GET",
            "/v1.1/devices/transactions",
            params=params,
            base_url=self.base_url
        )
        return DeviceTransactionListResponse(**response_data)

    def get_device_details(self, terminal_id: str) -> DeviceDetail:
        """
        Get device details.

        Args:
            terminal_id: The unique terminal identifier of the POS device

        Returns:
            DeviceDetail: Device details object
        """
        response_data = self.client.request(
            "GET",
            f"/v1.1/devices/{terminal_id}",
            base_url=self.base_url
        )
        return DeviceDetail(**response_data)

    def get_receipt_details(self, payment_reference: str) -> ReceiptDetail:
        """
        Get receipt details for a transaction.

        Args:
            payment_reference: The unique reference of the transaction

        Returns:
            ReceiptDetail: Receipt details object
        """
        response_data = self.client.request(
            "GET",
            f"/v1.1/devices/receipt/{payment_reference}",
            base_url=self.base_url
        )
        return ReceiptDetail(**response_data)

    def list_device_transactions(
        self,
        terminal_id: str,
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        from_amount: Optional[float] = None,
        to_amount: Optional[float] = None,
        rrn: Optional[str] = None,
        stan: Optional[str] = None,
        reference_number: Optional[str] = None
    ) -> DeviceTransactionListResponse:
        """
        List transactions for a specific device.

        Args:
            terminal_id: The unique terminal identifier of the POS device
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            from_date: Starting date in format YYYY-MM-DD (optional)
            to_date: End date in format YYYY-MM-DD (optional)
            from_amount: Minimum transaction amount (optional)
            to_amount: Maximum transaction amount (optional)
            rrn: Filter by RRN value (optional)
            stan: Filter by STAN value (optional)
            reference_number: Filter by reference number (optional)

        Returns:
            DeviceTransactionListResponse: Object containing list of device transactions and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date
        if from_amount is not None:
            params["from_amount"] = from_amount
        if to_amount is not None:
            params["to_amount"] = to_amount
        if rrn is not None:
            params["rrn"] = rrn
        if stan is not None:
            params["stan"] = stan
        if reference_number is not None:
            params["reference_number"] = reference_number
        
        response_data = self.client.request(
            "GET",
            f"/v1.1/devices/{terminal_id}/transactions",
            params=params,
            base_url=self.base_url
        )
        return DeviceTransactionListResponse(**response_data)

    def refund(
        self,
        terminal_id: str,
        reference_number: str,
        amount: float
    ) -> None:
        """
        Issue a refund for a device transaction.

        Args:
            terminal_id: The unique terminal identifier of the POS device
            reference_number: The reference number that was set for the original transaction
            amount: The amount to refund (must be <= original transaction amount)

        Returns:
            None: Empty response if refund was issued successfully
        """
        data = {
            "reference_number": reference_number,
            "amount": amount
        }
        
        self.client.request(
            "POST",
            f"/v1.1/devices/{terminal_id}/refund",
            json=data,
            base_url=self.base_url
        )
