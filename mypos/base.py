import logging
import os
import base64
import uuid
import niquests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class BaseClient:
    """
    Base Client for interacting with the MyPOS API.
    Handles authentication and basic request logic.
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
        """
        if not self.access_token:
            self.get_access_token()

    def _refresh_token_if_needed(self, response) -> bool:
        """
        Check if the token needs refresh based on response and refresh if needed. 
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

    def request(self, method: str, endpoint: str, params: dict = None, json: dict = None, data: dict = None, base_url: str = None) -> dict:
        """
        Make an authenticated request to the API.
        """
        url = f"{base_url or self.api_base_url}{endpoint}"
        
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": f"Bearer {self.access_token}",
            "API-Key": self.client_id,
        }
        
        if json is not None:
            headers["Content-Type"] = "application/json"
        elif data is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            headers["Content-Type"] = "application/json"
        
        response = niquests.request(method, url, headers=headers, params=params, json=json, data=data)
        
        if self._refresh_token_if_needed(response):
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = niquests.request(method, url, headers=headers, params=params, json=json, data=data)
            
        if response.status_code not in [200, 204]:
            logger.error(f"Request failed: {response.text}")
            raise Exception(f"Request failed: {response.text}")
            
        if response.status_code == 204:
            return {}
            
        return response.json()
