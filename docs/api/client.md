# Client & Authentication

## MyPOS Client

The `MyPOS` class is the main entry point for the SDK. It initializes all sub-modules.

```python
class MyPOS(BaseClient):
    def __init__(self):
        ...
```

### Accessing Modules

- `client.transactions`: Access transaction APIs (`v1`, `v1_1`).
- `client.devices`: Access device APIs (`v1`, `v1_1`).
- `client.webhooks`: Access webhook APIs (`v1`, `v1_1`).
- `client.psd2`: Access PSD2 APIs (`v1`).

## BaseClient

The `BaseClient` handles the low-level HTTP requests and authentication.

### Methods

#### `get_access_token() -> str`
Obtains a new access token from the MyPOS OAuth endpoint.

#### `request(method, endpoint, params=None, json=None, data=None, base_url=None) -> dict`
Makes an authenticated request to the API.
- Handles token refresh on 401 or 503 errors.
- Automatically adds `Authorization` and `X-Request-ID` headers.
