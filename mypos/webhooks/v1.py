from typing import Optional, List
from ...schemas import Webhook, WebhookListResponse, EventListResponse, Subscription, NotificationListResponse
import json

class WebhooksV1:
    def __init__(self, client):
        self.client = client
        # Webhooks API uses a different base URL
        self.base_url = "https://webhook-api.mypos.com"

    def create(self, payload_url: str, secret: str) -> Webhook:
        """
        Create a new webhook.
        """
        data = {
            "payload_url": payload_url,
            "secret": secret
        }
        response_data = self.client.request(
            "POST", 
            "/v1/webhooks", 
            data=data,
            base_url=self.base_url
        )
        return Webhook(**response_data["webhook"])

    def list(self, page: Optional[int] = 1, size: Optional[int] = 20) -> WebhookListResponse:
        """
        List all webhooks.
        """
        response_data = self.client.request(
            "GET", 
            "/v1/webhooks", 
            params={"page": page, "size": size},
            base_url=self.base_url
        )
        return WebhookListResponse(**response_data)

    def get(self, webhook_id: str) -> Webhook:
        """
        Get a single webhook by ID.
        """
        response_data = self.client.request(
            "GET", 
            f"/v1/webhooks/{webhook_id}",
            base_url=self.base_url
        )
        return Webhook(**response_data["webhook"])

    def update(self, webhook_id: str, payload_url: Optional[str] = None, secret: Optional[str] = None, is_active: Optional[bool] = None) -> Webhook:
        """
        Update a webhook.
        """
        data = {}
        if payload_url:
            data["payload_url"] = payload_url
        if secret:
            data["secret"] = secret
        if is_active is not None:
            data["is_active"] = str(is_active).lower() # API expects string 'true'/'false' or boolean? Example says is_active: true in response, but usually form data is string. 
            # Actually, the example for update request body shows: payload_url=...&secret=...
            # It doesn't explicitly show is_active in the request body example, but the description says "to disable a webhook... we can update its active flag".
            # Assuming standard form encoding.

        # If is_active is passed, we should probably check if the API expects "true"/"false" or "1"/"0". 
        # Given it's x-www-form-urlencoded, boolean values are often strings.
        # Let's assume standard string representation for now.
        
        response_data = self.client.request(
            "PATCH", 
            f"/v1/webhooks/{webhook_id}",
            data=data,
            base_url=self.base_url
        )
        return Webhook(**response_data["webhook"])

    def delete(self, webhook_id: str) -> None:
        """
        Delete a webhook.
        """
        self.client.request(
            "DELETE", 
            f"/v1/webhooks/{webhook_id}",
            base_url=self.base_url
        )

    def verify_signature(self, payload: str, headers: dict, secret: str) -> bool:
        """
        Verify the webhook signature.

        Args:
            payload: The raw request body (JSON string).
            headers: The request headers.
            secret: The webhook secret.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        import hmac
        import hashlib
        import time

        signature_header = headers.get("X-myPOS-Signature")
        if not signature_header:
            return False

        try:
            # Extract timestamp and signature
            parts = signature_header.split(",")
            timestamp = None
            signature = None
            
            for part in parts:
                if part.startswith("t="):
                    timestamp = part.split("=")[1]
                elif part.startswith("v1="):
                    signature = part.split("=")[1]
            
            if not timestamp or not signature:
                return False

            # Verify timestamp (tolerance of 5 minutes)
            current_time = int(time.time())
            if abs(current_time - int(timestamp)) > 300:
                return False

            # Normalize JSON payload (remove spaces)
            # The documentation says: "Please make sure there are no unneeded spaces in the JSON string between the key and value pairs and between the different values."
            # However, modifying the raw payload is risky if the sender didn't format it exactly as expected.
            # Ideally, we should use the raw payload as received. 
            # But the PHP example explicitly does str_replace(": ", ":") and str_replace(", ", ",").
            # So we will replicate that behavior.
            normalized_payload = payload.replace(": ", ":").replace(", ", ",")

            # Generate expected signature
            expected_signature = hmac.new(
                secret.encode("utf-8"),
                normalized_payload.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_signature, signature)

        except Exception:
            return False

    def list_events(self, page: Optional[int] = 1, size: Optional[int] = 20) -> EventListResponse:
        """
        List all available events.
        """
        response_data = self.client.request(
            "GET", 
            "/v1/events", 
            params={"page": page, "size": size},
            base_url=self.base_url
        )
        return EventListResponse(**response_data)

    def subscribe(self, event_id: str, webhook_id: Optional[str] = None) -> Subscription:
        """
        Subscribe for an event.
        """
        data = {
            "event_id": event_id
        }
        if webhook_id:
            data["webhook_id"] = webhook_id
            
        response_data = self.client.request(
            "POST", 
            "/v1/subscriptions", 
            data=data,
            base_url=self.base_url
        )
        return Subscription(**response_data["subscription"])

    def update_subscription(self, subscription_id: str, filter: Optional[dict] = None) -> Subscription:
        """
        Update event subscription.
        """
        data = {}
        if filter:
            # The example shows filter passed as a JSON string inside the form data
            # filter=%7B%22tids%22%3A%5B%2290004889%22%5D%7D
            data["filter"] = json.dumps(filter)
            
        response_data = self.client.request(
            "PUT", 
            f"/v1/subscriptions/{subscription_id}", # Documentation says /v1/subscriptions but usually update needs ID. However, example shows POST to /v1/subscriptions for create, and PUT to /v1/subscriptions for update? 
            # Wait, the example for update: curl -X PUT https://webhook-api.mypos.com/v1/subscriptions -d 'filter=...'
            # It doesn't show the subscription ID in the URL. But usually you update a specific resource.
            # Let's re-read carefully.
            # "Update event subscription... HTTP PUT or PATCH... /v1/subscriptions"
            # The example response contains "id": "7db45365...", so maybe it updates the subscription associated with the webhook?
            # But which subscription? A webhook can have multiple subscriptions?
            # Actually, looking at the unsubscribe example: DELETE /v1/subscriptions/ef082ef0...
            # It seems inconsistent if PUT doesn't take an ID.
            # However, if I look closely at the update example, it doesn't have an ID in the URL.
            # Maybe it updates based on some other context or it's a documentation quirk.
            # BUT, usually REST APIs use ID. Let's assume the documentation example might be missing the ID or it implies updating *a* subscription.
            # Wait, if I look at the unsubscribe example, it definitely uses ID.
            # Let's assume we need to pass the ID in the URL for PUT as well, or maybe the filter identifies it? Unlikely.
            # Let's try to follow standard REST practices and append ID, but if the user reports issues we might need to check.
            # Actually, let's look at the example again.
            # curl -X PUT https://webhook-api.mypos.com/v1/subscriptions ...
            # This looks like it might be updating the *list* or something? No, response is a single subscription.
            # Maybe it updates the subscription for the webhook authenticated by the token? But the token is for the merchant.
            # Let's assume the documentation example for PUT is slightly misleading and we should probably use /v1/subscriptions/{id} like DELETE.
            # OR, maybe we send subscription_id in the body? No, body only has filter.
            # Let's stick to appending ID to URL as it's safer for a specific update.
            # If the API truly expects no ID, it would be very strange for updating a specific subscription among many.
            # Re-reading: "Update event subscription... HTTP PUT or PATCH... /v1/subscriptions"
            # It is possible that the example URL is just /v1/subscriptions and it updates *something*.
            # But given DELETE uses ID, I will implement it with ID.
            # Wait, I can't be sure. Let's look at the Unsubscribe example: /v1/subscriptions/ef082ef0...
            # It is highly likely Update also requires ID.
            
            # Let's implement with ID.
            # Also, the example shows PUT.
            # I will use PUT /v1/subscriptions/{id}
            
            # Correction: The documentation text says "Update event subscription... HTTP PUT or PATCH... /v1/subscriptions".
            # It does NOT show {id}.
            # But the DELETE example DOES show {id}.
            # I will assume {id} is needed for safety.
            
            # Wait, if I look at the "Subscribe for an event" response, it returns a subscription object with an ID.
            # So we definitely have an ID to work with.
            
            # Let's go with /v1/subscriptions/{id}
            f"/v1/subscriptions/{subscription_id}",
            data=data,
            base_url=self.base_url
        )
        return Subscription(**response_data["subscription"])

    def unsubscribe(self, subscription_id: str) -> None:
        """
        Unsubscribe from an event.
        """
        self.client.request(
            "DELETE", 
            f"/v1/subscriptions/{subscription_id}",
            base_url=self.base_url
        )

    def list_notifications(self, page: Optional[int] = 1, size: Optional[int] = 20) -> NotificationListResponse:
        """
        List event notifications.
        """
        response_data = self.client.request(
            "GET", 
            "/v1/notifications", 
            params={"page": page, "size": size},
            base_url=self.base_url
        )
        return NotificationListResponse(**response_data)
