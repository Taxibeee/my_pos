from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TransactionType(Enum):
    FEE = "001"
    CASH_WITHDRAWAL = "002"
    OUTGOING_BANK_TRANSFER = "003"
    BALANCE_TRANSFER = "004"
    E_MONEY_REDEMPTION = "005"
    ACCOUNT_FUNDING = "006"
    ORIGINAL_CREDIT = "007"
    POS_PURCHASE = "008"
    ONLINE_PURCHASE = "009"
    INTERNAL_TRANSFER = "010"
    REFUND = "011"
    MONEY_REQUEST = "012"
    PAYMENT = "013"
    DIRECT_DEBIT = "014"
    PRE_AUTHORIZATION = "015"
    MOTO_PAYMENT = "016"
    MOTO_REFUND = "017"
    MOTO_PRE_AUTHORIZATION = "018"
    ATM_DEPOSIT = "019"
    NFC_PAYMENT = "022"
    ATM_SURCHARGE = "023"
    WITHDRAWAL = "024"
    UTILITY_BILLS = "026"
    PAYMENT_REQUEST = "035"
    PAYMENT_RETURN = "036"
    REVERSE_WITH_HOLD = "037"
    REVERSE_RELEASE = "038"
    COMMISSION = "039"
    CASH_FUNDING = "040"
    NEGATIVE_SET_OFF = "041"
    CHARGE_BACK = "042"
    PAYMENT_ON_POS = "501"

class ReferenceNumberType(int, Enum):
    REFERENCE_NUMBER = 1
    INVOICE_NUMBER = 2
    PRODUCT_ID = 3
    RESERVATION_NUMBER = 4

class PaymentButtonStatus(int, Enum):
    ACTIVE = 1
    DISABLED = 2

class PaymentLinkStatus(int, Enum):
    ACTIVE = 1
    DISABLED = 2
    EXPIRED = 4

class PaymentRequestStatus(int, Enum):
    PENDING = 1
    SEEN = 2
    FAILED = 3
    PAID = 4
    EXPIRED = 5
    CANCELLED = 6

class Transaction(BaseModel):
    id: Optional[int] = Field(None, description="The unique id of the transaction")
    payment_reference: str = Field(..., description="A unique reference of the transactions")
    transaction_type: Optional[TransactionType] = Field(None, description="The type of the transaction")
    transaction_amount: float = Field(..., description="The amount of the transaction")
    transaction_currency: str = Field(..., description="The currency of the receiving account. 3 character ISO 4217 code")
    original_amount: float = Field(..., description="The amount for which the transaction was initiated")
    original_currency: str = Field(..., description="The currency in which the transaction was initiated. 3 character ISO 4217 code")
    sign: str = Field(..., description="Permitted codes are 'booked', 'pending' and 'both' or 'C'/'D'")
    date: str = Field(..., description="The date of the transaction")
    operation_type: Optional[str] = Field(None, description="The type of the operation")
    reference_number: Optional[str] = Field(None, description="An optional custom reference number set for POS transaction")
    reference_number_type: Optional[ReferenceNumberType] = Field(None, description="Type of reference number")
    terminal_id: Optional[str] = Field(None, description="The TID of the POS device")
    serial_number: Optional[str] = Field(None, description="The serial number of the POS device")
    account_number: Optional[str] = Field(None, description="The identifier of the settlement account")
    ruid: Optional[str] = Field(None, description="Unique identifier of the submitted request")
    billing_descriptor: Optional[str] = Field(None, description="Merchant billing descriptor")
    pan: Optional[str] = Field(None, description="Last four digits of the card number")

class TransactionDetail(BaseModel):
    label: str = Field(..., description="The type of the detail or the title of a section of details")
    value: str = Field(..., description="The value of the detail")

class TransactionDetailsResponse(BaseModel):
    details: List[TransactionDetail] = Field(..., description="A list of transaction detail objects")

class TransactionDetails(BaseModel):
    reference: str = Field(..., description="The 'payment_reference' of the transaction")
    general: Dict[str, Any] = Field(..., description="Contains general information of the transaction")
    details: List[TransactionDetail] = Field(..., description="A list with details related to the transaction")

class MultipleTransactionDetailsResponse(BaseModel):
    transactions_details: List[TransactionDetails] = Field(..., description="An array of transaction details")

class Account(BaseModel):
    account_number: str = Field(..., description="A unique identifier of the account")
    iban: str = Field(..., description="The IBAN associated with the account")
    currency: str = Field(..., description="The currency of the account")
    name: str = Field(..., description="A custom name of the account")
    is_reserve: bool = Field(..., description="A flag describing whether the account is a reserve one or not")

class Pagination(BaseModel):
    page: int = Field(..., description="The page number")
    page_size: Optional[int] = Field(None, description="The number of items per page (v1.1)")
    size: Optional[int] = Field(None, description="The number of items per page (v1.0)")
    total: int = Field(..., description="Total number of records available")

class Language(BaseModel):
    code: str = Field(..., description="Language code in format: XX")
    description: str = Field(..., description="Full name of the language")

class PaymentButton(BaseModel):
    code: str = Field(..., description="Unique code of payment button")
    url: str = Field(..., description="Url address of payment button")
    custom_name: str = Field(..., description="Current name of the payment button")
    amount: float = Field(..., description="Total amount")
    currency: str = Field(..., description="Currency in which the payment button is operating")
    status: PaymentButtonStatus = Field(..., description="Current status of the payment button")

class PaymentLink(BaseModel):
    code: str = Field(..., description="Unique code of payment link")
    url: str = Field(..., description="Url address of payment link")
    custom_name: str = Field(..., description="Current name of the payment link")
    amount: float = Field(..., description="Total amount")
    currency: str = Field(..., description="Currency in which payment link is operating")
    status: PaymentLinkStatus = Field(..., description="Current status of the payment link")

class PaymentButtonDetails(BaseModel):
    created_on: str = Field(..., description="Date of payment button creation")
    code: str = Field(..., description="Unique code of payment button")
    url: str = Field(..., description="Url address of the payment button")
    custom_name: str = Field(..., description="Payment button name")
    item_name: str = Field(..., description="Item name")
    enable: bool = Field(..., description="Flag if this button is currently enabled or disabled")
    item_price: float = Field(..., description="Price of a single item")
    total_amount: float = Field(..., description="Multiplication of a single item price with quantity")
    quantity: int = Field(..., description="Items quantity")
    button_size: int = Field(..., description="Information about button size")
    send_sms: bool = Field(..., description="Receiving SMS when a purchase is processed")
    send_email: bool = Field(..., description="Receiving email when a purchase is processed")
    ask_for_customer_name: bool = Field(..., description="Require customer name on the payment page")
    ask_for_shipping_address: bool = Field(..., description="Require shipping address on the payment page")
    ask_for_customer_email: bool = Field(..., description="Require customer email on the payment page")
    ask_for_customer_phone_number: bool = Field(..., description="Require customer phone on the payment page")
    currency: str = Field(..., description="The currency of the account")
    pref_language: str = Field(..., description="Preferred language of the payment button")
    website: str = Field(..., description="Website address")
    cancel_url: str = Field(..., description="Customer will be redirected on this address when cancel request is executed")
    return_url: str = Field(..., description="Customer will be redirected on this address when retrun request is executed")
    account_number: str = Field(..., description="Account number which is related to this payment button")

class PaymentLinkDetails(BaseModel):
    created_on: str = Field(..., description="Date of payment link creation")
    code: str = Field(..., description="Unique code of payment link")
    url: str = Field(..., description="Url address of the payment link")
    custom_name: str = Field(..., description="Payment link name")
    item_name: str = Field(..., description="Item name")
    enable: bool = Field(..., description="Flag if this payment link is currently enabled or disabled")
    item_price: float = Field(..., description="Price of a single item")
    total_amount: float = Field(..., description="Multiplication of a single item price with quantity")
    quantity: int = Field(..., description="Items quantity")
    send_sms: bool = Field(..., description="Receiving SMS when a purchase is processed")
    send_email: bool = Field(..., description="Receiving email when a purchase is processed")
    ask_for_customer_name: bool = Field(..., description="Require customer name on the payment page")
    currency: str = Field(..., description="The currency of the account")
    pref_language: str = Field(..., description="Preferred language of the payment button")
    website: str = Field(..., description="Website address")
    account_number: str = Field(..., description="Account number which is related to this payment button")
    hide_quantity: bool = Field(..., description="If the quantity of items is hidden or not for customers")
    expire_date: str = Field(..., description="Date until this payment link will be active")

class PaymentRequest(BaseModel):
    code: str = Field(..., description="The code of the payment request")
    url: str = Field(..., description="Url address of created payment request")
    added_on: str = Field(..., description="The time and date when the payment request was created")
    client_name: str = Field(..., description="The name of the client to whom the payment request will be sent")
    amount: float = Field(..., description="The amount to be paid by the client")
    currency: str = Field(..., description="The currency, related to this payment request")
    reason: str = Field(..., description="A message shown to the client with the reason for the requested payment")
    booking_text: str = Field(..., description="Custom name of the payment request as seen in the myPOS account")
    status: PaymentRequestStatus = Field(..., description="Status of the payment request")

class PaymentRequestDetails(BaseModel):
    code: str = Field(..., description="The code of the payment request")
    url: str = Field(..., description="Url address of created payment request")
    added_on: str = Field(..., description="The time and date when the payment request was created")
    client_name: str = Field(..., description="The name of the client to whom the payment request will be sent")
    amount: float = Field(..., description="The amount to be paid by the client")
    currency: str = Field(..., description="The currency, related to this payment request")
    reason: str = Field(..., description="A message shown to the client with the reason for the requested payment")
    booking_text: str = Field(..., description="Custom name of the payment request as seen in the myPOS account")
    attempts: int = Field(..., description="Returns the attempts for payment by the client")
    expiry_on: str = Field(..., description="The time and date of expiry of the payment request")
    qr_generated: bool = Field(..., description="Show if the payment request is generated as QR code")
    email: str = Field(..., description="The email address to which the payment request was sent")
    gsm: str = Field(..., description="The phone number to which the payment request was sent")
    status: PaymentRequestStatus = Field(..., description="Status of the payment request")

class SettlementData(BaseModel):
    settlement_currency: str = Field(..., description="Settlement currency")
    account: Optional[Account] = Field(None, description="Current associated account with this settlement currency")

class TransactionListResponse(BaseModel):
    transactions: List[Transaction] = Field(..., description="A list of transaction objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class AccountListResponse(BaseModel):
    accounts: List[Account] = Field(..., description="A list of account objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class DeviceListResponse(BaseModel):
    devices: List[Device] = Field(..., description="A list of device objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class DeviceTransactionListResponse(BaseModel):
    transactions: List[DeviceTransaction] = Field(..., description="A list of device transaction objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class PaymentButtonListResponse(BaseModel):
    items: List[PaymentButton] = Field(..., description="A list of payment buttons")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class PaymentLinkListResponse(BaseModel):
    items: List[PaymentLink] = Field(..., description="A list of payment links")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class PaymentRequestListResponse(BaseModel):
    items: List[PaymentRequest] = Field(..., description="A list of payment requests")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class Device(BaseModel):
    terminal_id: str = Field(..., description="A unique number of the device")
    serial_number: str = Field(..., description="The serial number of the device")
    model: str = Field(..., description="The model of the device")

class DeviceDetail(BaseModel):
    last_transaction_date: str = Field(..., description="The date of the last transaction in format 'YYYY-MM-DD HH:mm:ss'")
    terminal_id: str = Field(..., description="The unique terminal identifier of the POS device")
    terminal_name: str = Field(..., description="The custom name of the POS device")
    serial_number: str = Field(..., description="The serial number of the POS device")
    model: str = Field(..., description="The model of the POS device")
    outlet_id: int = Field(..., description="The ID of the outlet to which the POS devices is assigned")
    outlet_name: str = Field(..., description="The name of the outlet to which the POS devices is assigned")
    device_currency: str = Field(..., description="The currency in which the POS device is operating in")
    status: str = Field(..., description="The status of the device")
    transactions_count: int = Field(..., description="The number of transactions processed on this POS device")
    settlement_account_number: str = Field(..., description="The number of the settlement account to which the POS device is assigned to")
    settlement_account_name: str = Field(..., description="The name of the settlement account to which the POS device is assigned to")
    settlement_account_currency: str = Field(..., description="The currency of the settlement account to which the POS device is assigned to")
    billing_descriptor: str = Field(..., description="The billing descriptor assigned to the POS device")
    receipt_footer_row_1: str = Field(..., description="The first row of the custom footer printed in the receipt")
    receipt_footer_row_2: str = Field(..., description="The second row of the custom footer printed in the receipt")
    forbidden_preauthorization: int = Field(..., description="A flag specifying wheter Pre-Authorizations are forbidden for this POS device")
    forbidden_moto: int = Field(..., description="A flag specifying wheter MOTO transactions are forbidden for this POS device")
    forbidden_reversal: int = Field(..., description="A flag specifying wheter reversal transactions are forbidden for this POS device")
    forbidden_refund: int = Field(..., description="A flag specifying wheter refund transactions are forbidden for this POS device")
    forbidden_topup: int = Field(..., description="A flag specifying wheter top-up transactions are forbidden for this POS device")
    card_topup_enabled: Optional[int] = Field(None, description="Flag for card topup enabled")
    receipt_address_preference: Optional[int] = Field(None, description="Receipt address preference")

class ReceiptDetail(BaseModel):
    is_declined: int = Field(..., description="A flag to determine whether the transactions has been declined")
    receipt_layout_version: int = Field(..., description="A enumrator of the layout version of the receipt")
    exchange_rate: Optional[str] = Field(None, description="The exchange rate if such has been applied")
    date: str = Field(..., description="The date of the transactions in format YYYY-MM-DD")
    time: str = Field(..., description="The time of the transaction in format HH:mm:ss")
    stan: str = Field(..., description="The stan of the transactions")
    terminal_id: str = Field(..., description="The TID of the POS device")
    merchant_id: str = Field(..., description="The ID of the merchant the POS device is related to")
    merchant_name: str = Field(..., description="The name of the merchant the POS device is related to")
    address_line_1: str = Field(..., description="The address printed on the first line")
    address_line_2: str = Field(..., description="The address printed on the second line")
    resp_code: Optional[str] = Field(None, description="The response code from the POS device")
    reference_number: str = Field(..., description="The reference number of the transaction")
    application_preferred_name: str = Field(..., description="The name of the card scheme application")
    installment_type: Optional[str] = Field(None, description="The type of the installment")
    installment_number: Optional[str] = Field(None, description="The number of the installment")
    installment_interest_rate: Optional[str] = Field(None, description="Installment interest rate")
    installment_first_amount: Optional[str] = Field(None, description="Installment first amount")
    installment_subseq_amount: Optional[str] = Field(None, description="Installment subseq amount")
    installment_annual_perc_rate: Optional[str] = Field(None, description="Installment annual percentage rate")
    installment_fee_rate: Optional[str] = Field(None, description="Installment fee rate")
    installment_total_amount: Optional[str] = Field(None, description="Installment total amount")
    transaction_preauth_code: str = Field(..., description="Installment pre-authorisation code")
    card_scheme: str = Field(..., description="The scheme of the used credit/debit card")
    pan: str = Field(..., description="The masked PAN of the card in format XXXX-XXXX-XXXX-1234")
    emboss_name: str = Field(..., description="The name on the card")
    amount: str = Field(..., description="The transaction amount")
    currency: str = Field(..., description="The transaction currency")
    auth_code: str = Field(..., description="The authorisation code")
    rrn: str = Field(..., description="The RRN of the transaction")
    aid: str = Field(..., description="The application identifier")
    amount_tip: Optional[str] = Field(None, description="The tip amount")
    amount_total: Optional[str] = Field(None, description="The total amount of the transactions")
    operator_code: str = Field(..., description="The operator code")
    dcc_amount: Optional[str] = Field(None, description="The DCC amount")
    dcc_currency: Optional[str] = Field(None, description="The DCC currency")
    tran_type: str = Field(..., description="The type of the transaction")
    sign_row_1: str = Field(..., description="The first signature row to printed")
    sign_row_2: str = Field(..., description="The second signature row to be printed")
    sign_row_3: str = Field(..., description="The third signature tow to be printed")
    exchange_rate_translation: Optional[str] = Field(None, description="Exchange rate translation")
    tran_status: str = Field(..., description="The status of the transaction")
    receipt_footer_row_1: Optional[str] = Field(None, description="The first row of the custom footer")
    receipt_footer_row_2: Optional[str] = Field(None, description="The second row of the custom footer")
    pl_card_balance: Optional[str] = Field(None, description="The balance of the private label card")
    pl_card_balance_currency: Optional[str] = Field(None, description="The currency of the private label card")

class DeviceTransaction(BaseModel):
    terminal_id: str = Field(..., description="The unique terminal identifier of the POS device")
    terminal_name: str = Field(..., description="The custom name of the POS device")
    outlet_name: str = Field(..., description="The name of the outlet to which the POS devices is assigned")
    amount: float = Field(..., description="The amount of the transaction")
    currency: str = Field(..., description="The currency of the receiving account. 3 character ISO 4217 code")
    fee: float = Field(..., description="The merhcnat fee for the transaction")
    pan: str = Field(..., description="The last 4 digits of the credit/debit card PAN")
    card_scheme: str = Field(..., description="The scheme of the presented debit/credit used for the transaction")
    rrn: str = Field(..., description="The RRN of the transcations")
    stan: str = Field(..., description="The stan of the transaction")
    date: str = Field(..., description="The date and time on which the transactions ocurred in format 'YYYY-MM-DD HH:mm:ss'")
    settlement_date: str = Field(..., description="The settlement date of the transaction in format 'YYYY-MM-DD HH:mm:ss'")
    settlement_amount: str = Field(..., description="The settled transaction amount")
    settlement_currency: str = Field(..., description="The currency of the settlement account")
    tran_status: str = Field(..., description="The status of the transaction")
    payment_status: str = Field(..., description="The status of the payment")
    payment_reference: str = Field(..., description="The payment reference of successfully settled transactions")
    reference_number: Optional[str] = Field(None, description="The reference number of a transaction. Can be filtered by custom client reference")

class WebhookEvent(BaseModel):
    id: str = Field(..., description="The ID of the event")
    name: str = Field(..., description="The name of the event")

class Webhook(BaseModel):
    id: str = Field(..., description="The unique ID of the webhook")
    created_on: str = Field(..., description="Creation date")
    is_active: bool = Field(..., description="Status of the webhook")
    payload_url: str = Field(..., description="The payload URL")
    secret: str = Field(..., description="The secret used to sign the callback")
    events: Optional[List[WebhookEvent]] = Field(None, description="List of events subscribed to")

class WebhookListResponse(BaseModel):
    webhooks: List[Webhook] = Field(..., description="A list of webhook objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class Event(BaseModel):
    id: str = Field(..., description="The ID of the event")
    name: str = Field(..., description="The name of the event")

class EventListResponse(BaseModel):
    events: List[Event] = Field(..., description="A list of event objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class Subscription(BaseModel):
    id: str = Field(..., description="The ID of the subscription")
    created_on: str = Field(..., description="Creation date")
    event: str = Field(..., description="The event name")
    filter: Optional[dict] = Field(None, description="The filter for the subscription")
    hook: Webhook = Field(..., description="The webhook object")

class SubscriptionListResponse(BaseModel):
    subscriptions: List[Subscription] = Field(..., description="A list of subscription objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")

class Notification(BaseModel):
    event: str = Field(..., description="Event's name")
    payload: dict = Field(..., description="Payload")
    sent_on: str = Field(..., description="Sent on")
    response_code: int = Field(..., description="Response status")
    retry_count: int = Field(..., description="Retry count")
    url: str = Field(..., description="URL")

class NotificationListResponse(BaseModel):
    notifications: List[Notification] = Field(..., description="A list of notification objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")