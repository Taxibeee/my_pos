# MyPOS Python SDK

A Python SDK for interacting with the MyPOS API.

## Documentation

Full documentation is available in the [docs](docs/) directory.

- [Getting Started](docs/README.md)
- [Setup & Configuration](docs/setup.md)
- [API Reference](docs/api/index.md)

## Installation

```bash
pip install .
```

## Quick Example

```python
from mypos import MyPOS

client = MyPOS()
devices = client.devices.v1_1.list()
print(devices)
```
