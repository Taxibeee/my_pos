from dotenv import load_dotenv
import base64
import niquests
import os

load_dotenv()

client_id = os.getenv("MYPOS_CLIENT_ID")
client_secret = os.getenv("MYPOS_CLIENT_SECRET")
auth_base_url = os.getenv("MYPOS_AUTH_BASE_URL")
x_request_id = os.getenv("X_REQUEST_ID")


def get_access_token() -> str:
    auth_url = f"{auth_base_url}/oauth/token"
    auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    }
    auth_data = {"grant_type": "client_credentials"}
    auth_response = niquests.post(auth_url, headers=auth_headers, data=auth_data)
    return auth_response.json().get("access_token")

print(get_access_token())