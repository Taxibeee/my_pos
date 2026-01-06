# Transactions & Online Payments

The Transactions module enables transaction management, account information retrieval, and handling of online payment methods like buttons, links, and payment requests.

## Access

```python
# V1
client.transactions.v1

# V1.1
client.transactions.v1_1
```

## Transactions V1.1 (Comprehensive)

### Transaction Management

#### `list`
List transactions with various filters.

```python
def list(
    self,
    page: Optional[int] = 1,
    size: Optional[int] = 20,
    order: Optional[int] = 1, # 1: Desc, 0: Asc
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    transaction_types: Optional[List[TransactionType]] = None,
    start_trn_id: Optional[int] = None
) -> TransactionListResponse
```

#### `get_details`
Get details of a single transaction.

```python
def get_details(self, payment_reference: str) -> TransactionDetailsResponse
```

#### `get_multiple_details`
Get details of up to 5 transactions.

```python
def get_multiple_details(self, payment_references: List[str]) -> MultipleTransactionDetailsResponse
```

### Accounts

#### `list_accounts`
List available accounts.

```python
def list_accounts(
    self, 
    page: Optional[int] = 1, 
    size: Optional[int] = 20
) -> AccountListResponse
```

#### `generate_mt940_statement`
Generate MT940 statement for an account.

```python
def generate_mt940_statement(
    self,
    document_type: int, # 0: Multicash, 1: Swift, 2: Structured
    date: str, # YYYY-MM-DD
    account_number: str
) -> str
```

### Payment Buttons

Manages "Pay Now" style buttons.

- `create_payment_button(...) -> dict`
- `update_payment_button(code, ...) -> PaymentButtonDetails`
- `list_payment_buttons(params) -> PaymentButtonListResponse`
- `get_payment_button_details(code) -> PaymentButtonDetails`
- `delete_payment_button(code)`

### Payment Links

Manages reusable payment links.

- `create_payment_link(...) -> dict`
- `update_payment_link(code, ...) -> PaymentLinkDetails`
- `list_payment_links(params) -> PaymentLinkListResponse`
- `get_payment_link_details(code) -> PaymentLinkDetails`
- `delete_payment_link(code)`

### Payment Requests

Manages requests for payment sent to customers.

- `create_payment_request(...) -> dict`
- `list_payment_requests(...) -> PaymentRequestListResponse`
- `get_payment_request_details(code) -> PaymentRequestDetails`
- `send_payment_request_reminder(code, ...)`

### Utilities

- `list_languages() -> List[Language]`: Get supported languages.
- `get_settlement_data() -> List[SettlementData]`: Get settlement accounts.

## Transactions V1

### `list`
```python
def list(
    self, 
    size: Optional[int] = 20,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    transaction_types: Optional[List[TransactionType]] = None,
    sign: Optional[str] = None,
    last_transaction_id: Optional[str] = None
) -> TransactionListResponse
```

### `get_details`
```python
def get_details(self, payment_reference: str) -> TransactionDetailsResponse
```
