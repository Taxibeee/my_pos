import logging
from dotenv import load_dotenv
import os
import niquests
import base64
from typing import Optional, List
from datetime import datetime, timedelta
import uuid
from .schemas import Transaction, TransactionType, TransactionListResponse

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

    def _refresh_token_if_needed(self, response) -> bool:
        """
        Check if the token needs refresh based on response and refresh if needed. 

        Analyses the API response to determine if the access token has expired or is invalid. If so, automatically refreshes the token.

        Args:
            response: The HTTP Response object from the API request. 

        Returns:
            bool: True if token was refreshed, False otherwise. 

        Note:
            Check for HTTP 401 status code or response code 503 to detect token expiration or invalidity. 
        """

        try:
            response_data = response.json()
            # Check for 503 or token-related errors
            if response.status_code == 401 or response_data.get('code') == 503:
                logger.warning("Access token expired or invalid, refreshing...")
                self.access_token = self.get_access_token()
                return True
        except Exception as e:
            # If response if not JSON or parsing fails, check status code
            if response.status_code == 401:
                logger.warning("Access token expired or invalid, refreshing...")
                self.access_token = self.get_access_token()
                return True
        return False

    def get_transactions(
        self, 
        page: Optional[int] = 1,
        size: Optional[int] = 20,
        order: Optional[int] = 1,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        transaction_types: Optional[List[TransactionType]] = None,
        start_trn_id: Optional[int] = None
    ) -> TransactionListResponse:
        """
        Get transactions from MyPOS API.

        Args:
            page: Page number. Default is 1.
            size: Number of items per page. Default is 20.
            order: Order of the transactions. 1-> Descending, 0-> Ascending. Default is 1.
            from_date: Start date of the transactions.
            to_date: End date of the transactions.
            transaction_types: List of transaction types.
            start_trn_id: Start transaction ID.

        Returns:
            TransactionListResponse: Object containing list of transactions and pagination info.
        """
        url = f"{self.api_base_url}/v1.1/transactions"
        
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": f"Bearer {self.access_token}",
            "API-Key": self.client_id,
            "Content-Type": "application/json"
        }
        
        params = {
            "page": page,
            "size": size,
            "order": order
        }
        
        if from_date:
            params["from_date"] = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if to_date:
            params["to_date"] = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if transaction_types:
            params["transaction_types"] = ",".join([t.value for t in transaction_types])
        if start_trn_id:
            params["start_trn_id"] = start_trn_id
            
        response = niquests.get(url, headers=headers, params=params)
        
        if self._refresh_token_if_needed(response):
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = niquests.get(url, headers=headers, params=params)
            
        if response.status_code != 200:
            logger.error(f"Failed to get transactions: {response.text}")
            raise Exception(f"Failed to get transactions: {response.text}")
            
        return TransactionListResponse(**response.json())




def create_client() -> Client:
    mypos_client: Client = Client()
    return mypos_client