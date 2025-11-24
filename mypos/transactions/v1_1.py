from typing import Optional, List
from datetime import datetime
from ...schemas import MultipleTransactionDetailsResponse, AccountListResponse, TransactionType, TransactionListResponse, TransactionDetailsResponse, Language, PaymentButtonListResponse, PaymentButtonStatus, PaymentLinkListResponse, PaymentLinkStatus, PaymentButtonDetails, PaymentLinkDetails, SettlementData, PaymentRequestDetails, PaymentRequestListResponse, PaymentRequestStatus

class TransactionsV1_1:
    def __init__(self, client):
        self.client = client

    def list(
        self, 
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        order: Optional[int] = 1,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        transaction_types: Optional[List[TransactionType]] = None,
        start_trn_id: Optional[int] = None
    ) -> TransactionListResponse:
        """
        Get transactions from MyPOS API (v1.1).

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            order: Order of the transactions. 1-> Descending, 0-> Ascending. Default is 1.
            from_date: Start date of the transactions.
            to_date: End date of the transactions.
            transaction_types: List of transaction types.
            start_trn_id: Start transaction ID.

        Returns:
            TransactionListResponse: Object containing list of transactions and pagination info.
        """
        params = {
            "page": page,
            "size": size,
            "order": order
        }
        
        if from_date:
            params["from_date"] = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if to_date:
            params["to_date"] = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if transaction_types:
            params["transaction_types"] = ",".join([t.value for t in transaction_types])
        if start_trn_id:
            params["start_trn_id"] = start_trn_id

        response_data = self.client.request(
            "GET", 
            "/v1.1/transactions", 
            params=params
        )
        return TransactionListResponse(**response_data)

    def get_details(self, payment_reference: str) -> TransactionDetailsResponse:
        """
        Get transaction details from MyPOS API (v1.1).
        """
        response_data = self.client.request("GET", f"/v1.1/transactions/{payment_reference}")
        return TransactionDetailsResponse(**response_data)

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

    def generate_mt940_statement(
        self,
        document_type: int,
        date: str,
        account_number: str
    ) -> str:
        """
        Generate MT940 statement for an account.

        Args:
            document_type: The type of the MT940. 0 = Multicash, 1 = Swift, 2 = Structured
            date: The date for which to generate the statement in format YYYY-MM-DD
            account_number: The number of the account for which to generate the statement

        Returns:
            str: The contents of the MT940 generated file
        """
        data = {
            "document_type": document_type,
            "date": date,
            "account_number": account_number
        }
        
        response_data = self.client.request(
            "POST",
            "/v1.1/accounts/statement",
            json=data
        )
        
        # The response is a plain string (MT940 file contents)
        return response_data if isinstance(response_data, str) else str(response_data)

    def create_payment_button(
        self,
        item_name: str,
        item_price: float,
        currency: str,
        custom_name: str,
        quantity: int,
        button_size: int,
        account_number: Optional[str] = None,
        pref_language: Optional[str] = None,
        website: Optional[str] = None,
        send_sms: Optional[bool] = None,
        send_email: Optional[bool] = None,
        ask_for_customer_name: Optional[bool] = None,
        ask_for_shipping_address: Optional[bool] = None,
        ask_for_customer_email: Optional[bool] = None,
        ask_for_customer_phone: Optional[bool] = None,
        cancel_url: Optional[str] = None,
        return_url: Optional[str] = None
    ) -> dict:
        """
        Create a payment button.

        Args:
            item_name: Item name
            item_price: Price of a single item
            currency: Currency (3 character ISO code)
            custom_name: Payment button name
            quantity: Items quantity (must be at least 1)
            button_size: 0 = Small, 1 = Big
            account_number: Account number (optional)
            pref_language: Preferred language in format 'XX' (optional)
            website: Website address (optional)
            send_sms: Receive SMS when purchase is processed (optional)
            send_email: Receive email when purchase is processed (optional)
            ask_for_customer_name: Require customer name on payment page (optional)
            ask_for_shipping_address: Require shipping address on payment page (optional)
            ask_for_customer_email: Require customer email on payment page (optional)
            ask_for_customer_phone: Require customer phone on payment page (optional)
            cancel_url: Redirect URL when cancel request is executed (optional)
            return_url: Redirect URL when return request is executed (optional)

        Returns:
            dict: Response containing the URL of the created payment button
        """
        data = {
            "item_name": item_name,
            "item_price": item_price,
            "currency": currency,
            "custom_name": custom_name,
            "quantity": quantity,
            "button_size": button_size
        }
        
        # Add optional parameters
        if account_number is not None:
            data["account_number"] = account_number
        if pref_language is not None:
            data["pref_language"] = pref_language
        if website is not None:
            data["website"] = website
        if send_sms is not None:
            data["send_sms"] = send_sms
        if send_email is not None:
            data["send_email"] = send_email
        if ask_for_customer_name is not None:
            data["ask_for_customer_name"] = ask_for_customer_name
        if ask_for_shipping_address is not None:
            data["ask_for_shipping_address"] = ask_for_shipping_address
        if ask_for_customer_email is not None:
            data["ask_for_customer_email"] = ask_for_customer_email
        if ask_for_customer_phone is not None:
            data["ask_for_customer_phone"] = ask_for_customer_phone
        if cancel_url is not None:
            data["cancel_url"] = cancel_url
        if return_url is not None:
            data["return_url"] = return_url
        
        return self.client.request(
            "POST",
            "/v1.1/online-payments/button",
            json=data
        )

    def create_payment_link(
        self,
        item_name: str,
        item_price: float,
        currency: str,
        account_number: str,
        custom_name: str,
        quantity: int,
        pref_language: Optional[str] = None,
        website: Optional[str] = None,
        send_sms: Optional[bool] = None,
        send_email: Optional[bool] = None,
        ask_for_customer_name: Optional[bool] = None,
        hide_quantity: Optional[bool] = None,
        expired_date: Optional[str] = None
    ) -> dict:
        """
        Create a payment link.

        Args:
            item_name: Item name
            item_price: Price of a single item
            currency: Currency (3 character ISO code)
            account_number: Account number
            custom_name: Payment link name
            quantity: Items quantity (must be at least 1)
            pref_language: Preferred language in format 'XX' (optional)
            website: Website address (optional)
            send_sms: Receive SMS when purchase is processed (optional)
            send_email: Receive email when purchase is processed (optional)
            ask_for_customer_name: Require customer name on payment page (optional)
            hide_quantity: Quantity should be hidden for customer (optional)
            expired_date: Date until payment link will be active in format YYYY-MM-DD (optional)

        Returns:
            dict: Response containing the URL of the created payment link
        """
        data = {
            "item_name": item_name,
            "item_price": item_price,
            "currency": currency,
            "account_number": account_number,
            "custom_name": custom_name,
            "quantity": quantity
        }
        
        # Add optional parameters
        if pref_language is not None:
            data["pref_language"] = pref_language
        if website is not None:
            data["website"] = website
        if send_sms is not None:
            data["send_sms"] = send_sms
        if send_email is not None:
            data["send_email"] = send_email
        if ask_for_customer_name is not None:
            data["ask_for_customer_name"] = ask_for_customer_name
        if hide_quantity is not None:
            data["hide_quantity"] = hide_quantity
        if expired_date is not None:
            data["expired_date"] = expired_date
        
        return self.client.request(
            "POST",
            "/v1.1/online-payments/link",
            json=data
        )

    def list_languages(self) -> List[Language]:
        """
        Get list of supported languages for payment buttons and links.

        Returns:
            List[Language]: List of supported languages
        """
        response_data = self.client.request(
            "GET",
            "/v1.1/online-payments/languages"
        )
        # Response is a list of language objects
        return [Language(**lang) for lang in response_data]

    def list_payment_buttons(
        self,
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        status: Optional[PaymentButtonStatus] = None
    ) -> PaymentButtonListResponse:
        """
        List payment buttons.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            status: Filter by payment button status (optional)

        Returns:
            PaymentButtonListResponse: Object containing list of payment buttons and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        if status is not None:
            params["status"] = status.value
        
        response_data = self.client.request(
            "GET",
            "/v1.1/online-payments/buttons",
            params=params
        )
        return PaymentButtonListResponse(**response_data)

    def list_payment_links(
        self,
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        status: Optional[PaymentLinkStatus] = None
    ) -> PaymentLinkListResponse:
        """
        List payment links.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            status: Filter by payment link status (optional)

        Returns:
            PaymentLinkListResponse: Object containing list of payment links and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        if status is not None:
            params["status"] = status.value
        
        response_data = self.client.request(
            "GET",
            "/v1.1/online-payments/links",
            params=params
        )
        return PaymentLinkListResponse(**response_data)

    def get_payment_button_details(self, code: str) -> PaymentButtonDetails:
        """
        Get payment button details.

        Args:
            code: Unique code of the payment button

        Returns:
            PaymentButtonDetails: Payment button details object
        """
        response_data = self.client.request(
            "GET",
            f"/v1.1/online-payments/button/{code}"
        )
        return PaymentButtonDetails(**response_data)

    def get_payment_link_details(self, code: str) -> PaymentLinkDetails:
        """
        Get payment link details.

        Args:
            code: Unique code of the payment link

        Returns:
            PaymentLinkDetails: Payment link details object
        """
        response_data = self.client.request(
            "GET",
            f"/v1.1/online-payments/link/{code}"
        )
        return PaymentLinkDetails(**response_data)

    def delete_payment_button(self, code: str) -> None:
        """
        Delete a payment button.

        Args:
            code: Unique code of the payment button

        Returns:
            None
        """
        self.client.request(
            "DELETE",
            f"/v1.1/online-payments/button/{code}"
        )

    def delete_payment_link(self, code: str) -> None:
        """
        Delete a payment link.

        Args:
            code: Unique code of the payment link

        Returns:
            None
        """
        self.client.request(
            "DELETE",
            f"/v1.1/online-payments/link/{code}"
        )

    def get_settlement_data(self) -> List[SettlementData]:
        """
        Get settlement data (list of settlement accounts).

        Returns:
            List[SettlementData]: List of settlement data objects
        """
        response_data = self.client.request(
            "GET",
            "/v1.1/online-payments/settlement-data"
        )
        # Response is a list of settlement data objects
        return [SettlementData(**item) for item in response_data]

    def update_payment_button(
        self,
        code: str,
        pref_lang: Optional[str] = None,
        custom_name: Optional[str] = None,
        send_sms: Optional[bool] = None,
        send_email: Optional[bool] = None,
        ask_for_customer_name: Optional[bool] = None,
        ask_for_customer_shipping_address: Optional[bool] = None,
        ask_for_customer_email: Optional[bool] = None,
        ask_for_customer_phone_number: Optional[bool] = None,
        website: Optional[str] = None,
        cancel_url: Optional[str] = None,
        return_url: Optional[str] = None,
        button_size: Optional[int] = None,
        enable: Optional[bool] = None
    ) -> PaymentButtonDetails:
        """
        Update a payment button.

        Args:
            code: Unique code of the payment button
            pref_lang: Preferred language in format 'XX' (optional)
            custom_name: Payment button name (optional)
            send_sms: Receive SMS when purchase is processed (optional)
            send_email: Receive email when purchase is processed (optional)
            ask_for_customer_name: Require customer name on payment page (optional)
            ask_for_customer_shipping_address: Require shipping address on payment page (optional)
            ask_for_customer_email: Require customer email on payment page (optional)
            ask_for_customer_phone_number: Require customer phone on payment page (optional)
            website: Website address (optional)
            cancel_url: Redirect URL when cancel request is executed (optional)
            return_url: Redirect URL when return request is executed (optional)
            button_size: 0 = Small, 1 = Big (optional)
            enable: Flag if button is enabled or disabled (optional)

        Returns:
            PaymentButtonDetails: Updated payment button details
        """
        data = {}
        
        # Add optional parameters
        if pref_lang is not None:
            data["pref_lang"] = pref_lang
        if custom_name is not None:
            data["custom_name"] = custom_name
        if send_sms is not None:
            data["send_sms"] = send_sms
        if send_email is not None:
            data["send_email"] = send_email
        if ask_for_customer_name is not None:
            data["ask_for_customer_name"] = ask_for_customer_name
        if ask_for_customer_shipping_address is not None:
            data["ask_for_customer_shipping_address"] = ask_for_customer_shipping_address
        if ask_for_customer_email is not None:
            data["ask_for_customer_email"] = ask_for_customer_email
        if ask_for_customer_phone_number is not None:
            data["ask_for_customer_phone_number"] = ask_for_customer_phone_number
        if website is not None:
            data["website"] = website
        if cancel_url is not None:
            data["cancel_url"] = cancel_url
        if return_url is not None:
            data["return_url"] = return_url
        if button_size is not None:
            data["button_size"] = button_size
        if enable is not None:
            data["enable"] = enable
        
        response_data = self.client.request(
            "PATCH",
            f"/v1.1/online-payments/button/{code}",
            json=data
        )
        return PaymentButtonDetails(**response_data)

    def update_payment_link(
        self,
        code: str,
        pref_lang: Optional[str] = None,
        custom_name: Optional[str] = None,
        send_sms: Optional[bool] = None,
        send_email: Optional[bool] = None,
        ask_for_customer_name: Optional[bool] = None,
        website: Optional[str] = None,
        enable: Optional[bool] = None,
        hide_quantity: Optional[bool] = None,
        expired_date: Optional[str] = None
    ) -> PaymentLinkDetails:
        """
        Update a payment link.

        Args:
            code: Unique code of the payment link
            pref_lang: Preferred language in format 'XX' (optional)
            custom_name: Payment link name (optional)
            send_sms: Receive SMS when purchase is processed (optional)
            send_email: Receive email when purchase is processed (optional)
            ask_for_customer_name: Require customer name on payment page (optional)
            website: Website address (optional)
            enable: Flag if link is enabled or disabled (optional)
            hide_quantity: Quantity should be hidden for customer (optional)
            expired_date: Date until payment link will be active in format YYYY-MM-DD (optional)

        Returns:
            PaymentLinkDetails: Updated payment link details
        """
        data = {}
        
        # Add optional parameters
        if pref_lang is not None:
            data["pref_lang"] = pref_lang
        if custom_name is not None:
            data["custom_name"] = custom_name
        if send_sms is not None:
            data["send_sms"] = send_sms
        if send_email is not None:
            data["send_email"] = send_email
        if ask_for_customer_name is not None:
            data["ask_for_customer_name"] = ask_for_customer_name
        if website is not None:
            data["website"] = website
        if enable is not None:
            data["enable"] = enable
        if hide_quantity is not None:
            data["hide_quantity"] = hide_quantity
        if expired_date is not None:
            data["expired_date"] = expired_date
        
        response_data = self.client.request(
            "PATCH",
            f"/v1.1/online-payments/link/{code}",
            json=data
        )
        return PaymentLinkDetails(**response_data)

    def create_payment_request(
        self,
        qr_generated: bool,
        amount: float,
        currency: str,
        client_name: Optional[str] = None,
        reason: Optional[str] = None,
        booking_text: Optional[str] = None,
        dba: Optional[str] = None,
        expired_date: Optional[str] = None,
        payment_request_lang: Optional[str] = None,
        notify_gsm: Optional[str] = None
    ) -> dict:
        """
        Create a payment request.

        Args:
            qr_generated: True for QR code payment request, False for normal payment request
            amount: The amount to be paid by the client
            currency: Currency (3 character ISO code)
            client_name: Name of the client (mandatory for normal PR, not for QR)
            reason: Message shown to client with reason for payment (optional)
            booking_text: Custom name as seen in myPOS account (optional)
            dba: Doing business as field shown in client's bank statement (optional)
            expired_date: Date until payment request is active in format YYYY-MM-DD (optional)
            payment_request_lang: Preferred language in format 'XX' (mandatory for normal PR)
            notify_gsm: Number to receive SMS when payment is processed (optional)

        Returns:
            dict: Response containing code and payment_request_url
        """
        data = {
            "qr_generated": qr_generated,
            "amount": amount,
            "currency": currency
        }
        
        # Add optional/conditional parameters
        if client_name is not None:
            data["client_name"] = client_name
        if reason is not None:
            data["reason"] = reason
        if booking_text is not None:
            data["booking_text"] = booking_text
        if dba is not None:
            data["dba"] = dba
        if expired_date is not None:
            data["expired_date"] = expired_date
        if payment_request_lang is not None:
            data["payment_request_lang"] = payment_request_lang
        if notify_gsm is not None:
            data["notify_gsm"] = notify_gsm
        
        return self.client.request(
            "POST",
            "/v1.1/online-payments/payment-request",
            json=data
        )

    def send_payment_request_reminder(
        self,
        code: str,
        gsm: Optional[str] = None,
        email: Optional[str] = None
    ) -> PaymentRequestDetails:
        """
        Send a payment request reminder.

        Args:
            code: The code of the payment request
            gsm: Phone number to send reminder (optional, at least one of gsm/email required)
            email: Email address to send reminder (optional, at least one of gsm/email required)

        Returns:
            PaymentRequestDetails: Payment request details object
        """
        data = {}
        
        if gsm is not None:
            data["gsm"] = gsm
        if email is not None:
            data["email"] = email
        
        response_data = self.client.request(
            "PATCH",
            f"/v1.1/online-payments/payment-request/{code}/reminder",
            json=data
        )
        return PaymentRequestDetails(**response_data)

    def list_payment_requests(
        self,
        page: Optional[int] = 1,
        size: Optional[int] = 8,
        status: Optional[PaymentRequestStatus] = None,
        code: Optional[str] = None,
        from_amount: Optional[float] = None,
        to_amount: Optional[float] = None,
        currency: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        client_name: Optional[str] = None,
        reason: Optional[str] = None,
        booking_text: Optional[str] = None
    ) -> PaymentRequestListResponse:
        """
        List payment requests.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 8.
            status: Filter by payment request status (optional)
            code: Filter by payment request code (optional)
            from_amount: Minimum amount filter (optional)
            to_amount: Maximum amount filter (optional)
            currency: Currency filter (optional, default EUR)
            from_date: Starting date filter (optional)
            to_date: End date filter (optional)
            client_name: Client name filter (optional)
            reason: Reason filter (optional)
            booking_text: Booking text filter (optional)

        Returns:
            PaymentRequestListResponse: Object containing list of payment requests and pagination info
        """
        params = {
            "page": page,
            "size": size
        }
        
        # Add optional filters
        if status is not None:
            params["status"] = status.value
        if code is not None:
            params["code"] = code
        if from_amount is not None:
            params["from_amount"] = from_amount
        if to_amount is not None:
            params["to_amount"] = to_amount
        if currency is not None:
            params["currency"] = currency
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date
        if client_name is not None:
            params["client_name"] = client_name
        if reason is not None:
            params["reason"] = reason
        if booking_text is not None:
            params["booking_text"] = booking_text
        
        response_data = self.client.request(
            "GET",
            "/v1.1/online-payments/payment-requests",
            params=params
        )
        return PaymentRequestListResponse(**response_data)

    def get_payment_request_details(self, code: str) -> PaymentRequestDetails:
        """
        Get payment request details.

        Args:
            code: Unique code of the payment request

        Returns:
            PaymentRequestDetails: Payment request details object
        """
        response_data = self.client.request(
            "GET",
            f"/v1.1/online-payments/payment-request/{code}"
        )
        return PaymentRequestDetails(**response_data)
