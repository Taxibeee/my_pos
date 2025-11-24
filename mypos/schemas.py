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
    id: int = Field(..., description="The unique id of the transaction")
    payment_reference: str = Field(..., description="A unique reference of the transactions")
    transaction_type: TransactionType = Field(..., description="The type of the transaction")
    transaction_amount: str = Field(..., description="The amount of the transaction after possible conversions")
    transaction_currency: str = Field(..., description="The currency of the receiving account. 3 character ISO 4217 code")
    original_amount: str = Field(..., description="The amount for which the transaction was initiated")
    original_currency: str = Field(..., description="The currency in which the transaction was initiated. 3 character ISO 4217 code")
    sign: str = Field(..., description="Permitted codes are 'booked', 'pending' and 'both'")
    date: str = Field(..., description="The date of the transaction")
    operation_type: str = Field(..., description="The type of the operation")
    reference_number: Optional[str] = Field(None, description="An optional custom reference number set for POS transaction")
    reference_number_type: Optional[ReferenceNumberType] = Field(None, description="Type of reference number")
    terminal_id: Optional[str] = Field(None, description="The TID of the POS device")
    serial_number: Optional[str] = Field(None, description="The serial number of the POS device")
    account_number: Optional[str] = Field(None, description="The identifier of the settlement account")
    ruid: Optional[str] = Field(None, description="Unique identifier of the submitted request")
    billing_descriptor: Optional[str] = Field(None, description="Merchant billing descriptor")
    pan: Optional[str] = Field(None, description="Last four digits of the card number")

class TransactionDetail(BaseModel):
    title: str = Field(..., description="The type of the detail or the title of a section of details")
    value: str = Field(..., description="The value of the detail")

class TransactionDetails(BaseModel):
    reference: str = Field(..., description="The 'payment_reference' of the transaction")
    general: Dict[str, Any] = Field(..., description="Contains general information of the transaction")
    details: List[TransactionDetail] = Field(..., description="A list with details related to the transaction")

class Account(BaseModel):
    account_number: str = Field(..., description="A unique identifier of the account")
    iban: str = Field(..., description="The IBAN associated with the account")
    currency: str = Field(..., description="The currency of the account")
    name: str = Field(..., description="A custom name of the account")
    is_reserve: bool = Field(..., description="A flag describing whether the account is a reserve one or not")

class Pagination(BaseModel):
    page: int = Field(..., description="The page number")
    page_size: int = Field(..., description="The number of items per page")
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
    expired_date: str = Field(..., description="Date until this payment link will be active")

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
    currency: str = Field(..., description="Settlement currency")
    account: Account = Field(..., description="Current associated account with this settlement currency")

class TransactionListResponse(BaseModel):
    transactions: List[Transaction] = Field(..., description="A list of transaction objects")
    pagination: Pagination = Field(..., description="Information about the paginated results")