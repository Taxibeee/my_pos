# MyPOS SDK Documentation

Welcome to the documentation for the MyPOS Python SDK. This SDK provides a simple and structured way to interact with the MyPOS API, covering Transactions, Devices, Webhooks, and PSD2 services.

## Overview

The SDK is organized into modules corresponding to MyPOS API sections:

- **Transactions**: Manage transactions, retrieve details, refund, etc.
- **Devices**: Manage POS devices, terminals, and activation.
- **Webhooks**: Manage webhook subscriptions and events.
- **PSD2**: Interface for PSD2 related operations.

## Quick Start

```python
from mypos import MyPOS

# Initialize the client (loads credentials from .env)
client = MyPOS()

# Example: Get list of POS devices
response = client.devices.v1_1.get_devices()
print(response)
```

## Documentation Structure

- [Setup & Configuration](setup.md): Installation and authentication setup.
- [API Reference](api/index.md): Detailed API reference for all modules.
- [Schemas](schemas.md): Data models and types used in the SDK.
