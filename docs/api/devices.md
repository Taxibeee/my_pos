# Devices

The Devices module allows you to manage POS devices, retrieve transactions, and issue refunds.

## Access

```python
# V1
client.devices.v1

# V1.1
client.devices.v1_1
```

## Devices V1.1 (Value Added)

### `list`
List all devices associated with the merchant account.

```python
def list(
    self,
    page: Optional[int] = 1,
    size: Optional[int] = 20,
    terminal_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    model: Optional[str] = None
) -> DeviceListResponse
```

### `list_transactions`
List transactions across all devices or filtered devices.

```python
def list_transactions(
    self,
    page: Optional[int] = 1,
    size: Optional[int] = 20,
    from_date: Optional[str] = None, # YYYY-MM-DD
    to_date: Optional[str] = None,   # YYYY-MM-DD
    from_amount: Optional[float] = None,
    to_amount: Optional[float] = None,
    rrn: Optional[str] = None,
    stan: Optional[str] = None,
    terminal_name: Optional[str] = None,
    reference_number: Optional[str] = None,
    terminal_id: Optional[str] = None
) -> DeviceTransactionListResponse
```

### `get_device_details`
Get details for a specific terminal.

```python
def get_device_details(self, terminal_id: str) -> DeviceDetail
```

### `list_device_transactions`
List transactions for a specific terminal.

```python
def list_device_transactions(
    self,
    terminal_id: str,
    page: Optional[int] = 1,
    size: Optional[int] = 20,
    ... # same filters as list_transactions
) -> DeviceTransactionListResponse
```

### `get_receipt_details`
Get receipt details for a transaction.

```python
def get_receipt_details(self, payment_reference: str) -> ReceiptDetail
```

### `refund`
Issue a refund for a transaction on a specific device.

```python
def refund(
    self, 
    terminal_id: str, 
    reference_number: str, 
    amount: float
) -> None
```

## Devices V1

### `list`

```python
def list(
    self, 
    size: Optional[int] = 20,
    terminal_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    model: Optional[str] = None
) -> DeviceListResponse
```

### `list_transactions`

```python
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
) -> DeviceTransactionListResponse
```

### `get_details`

```python
def get_details(self, terminal_id: str) -> DeviceDetail
```
