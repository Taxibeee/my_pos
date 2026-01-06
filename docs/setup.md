# Setup & Configuration

## Installation

You can install the package using `pip` or other package managers like `uv`.

### Using pip

```bash
pip install git+https://github.com/your-repo/mypos.git
```

### Using uv

```bash
uv pip install .
```

## Configuration

The SDK uses environment variables for configuration. You need to create a `.env` file in your project root or set these variables in your environment.

### `.env` Structure

```dotenv
# MyPOS Client Credentials
MYPOS_CLIENT_ID="your_client_id"
MYPOS_CLIENT_SECRET="your_client_secret"

# API Base URLs
MYPOS_AUTH_BASE_URL="https://mypos.com"
MYPOS_API_BASE_URL="https://mypos.com"

# Optional
X_REQUEST_ID="optional_default_request_id"
```

## Authentication

The `MyPOS` client automatically handles OAuth2 client credentials flow. It retrieves an access token using `MYPOS_CLIENT_ID` and `MYPOS_CLIENT_SECRET` and refreshes it automatically when needed.

```python
from mypos import MyPOS

client = MyPOS()
# The client will automatically authenticate when you make the first request.
```
