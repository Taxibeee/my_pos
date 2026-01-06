# Schemas

The SDK uses [Pydantic](https://docs.pydantic.dev/) models for data validation and structure. All response objects and complex parameters are defined in `mypos.schemas`.

## Key Enums

- **TransactionType**: Constants for transaction types (e.g., `POS_PURCHASE`, `REFUND`).
- **ReferenceNumberType**: Types of reference numbers.
- **PaymentButtonStatus**: Status for payment buttons (`ACTIVE`, `DISABLED`).
- **PaymentLinkStatus**: Status for payment links (`ACTIVE`, `DISABLED`, `EXPIRED`).
- **PaymentRequestStatus**: Status for payment requests (`PENDING`, `PAID`, `EXPIRED`, etc).

## Response Models

API methods return Pydantic models instead of raw dictionaries where possible.

- **TransactionListResponse**: List of transactions with pagination.
- **DeviceListResponse**: List of devices.
- **WebhookListResponse**: List of webhooks.
- **DeviceDetail**: Detailed information about a POS device.
- **TransactionDetails**: Detailed information about a transaction.

You can access fields using dot notation:

```python
response = client.devices.v1_1.list()
for device in response.data:
    print(device.terminal_id)
```

Or convert to a dictionary:

```python
data = response.model_dump()
```
