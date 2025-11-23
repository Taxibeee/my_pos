import logging
from dotenv import load_dotenv
import os
import niquests
import base64

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Client:
    """
    Client for interacting with the MyPOS API.

    This client handles authentication, token management, and provides methods
    to retrieve fleet orders, vehicles, drivers, and fleet state logs from
    the MyPOS API. It automatically manages access token refresh when tokens
    expire or become invalid.
    
    Attributes:
        client_id: OAuth client ID for authentication
        client_secret: OAuth client secret for authentication
        x_request_id: x-request-id header for the request
        auth_base_url: Base URL for the authentication API
        api_base_url: Base URL for the API
    """

    def __init__(self) -> None:
        self.client_id = os.getenv("MYPOS_CLIENT_ID")
        self.client_secret = os.getenv("MYPOS_CLIENT_SECRET")
        self.x_request_id = os.getenv("X_REQUEST_ID")
        self.auth_base_url = os.getenv("MYPOS_AUTH_BASE_URL")
        self.api_base_url = os.getenv("MYPOS_API_BASE_URL")
        self.access_token = None
        self._ensure_token()

    def get_access_token(self) -> str:
        """
        Get the access token for the client.
        """
        logger.info("Requesting access token from MyPOS API")
        auth_url = f"{self.auth_base_url}/oauth/token"
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic %s" % base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        }
        auth_data = {"grant_type": "client_credentials"}
        auth_response = niquests.post(auth_url, headers=auth_headers, data=auth_data)

        if auth_response.status_code != 200:
            logger.error(f"Failed to get access token: {auth_response.json()}")
            raise Exception(f"Failed to get access token: {auth_response.json()}")

        self.access_token = auth_response.json().get("access_token")
        if not self.access_token:
            logger.error("No access token found in response")
            raise Exception("No access token found in response")
        return self.access_token


    def _ensure_token(self) -> None:
        """
        Ensure that the client has a valid access token.

        Refresh if not configured. Private method that checks if an access token exists. If not,
        it automatically fetches a new token. This is called during
        initialization and before API requests.
        """
        if not self.access_token:
            self.get_access_token()
        