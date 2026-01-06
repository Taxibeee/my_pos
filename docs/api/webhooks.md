# Webhooks

The Webhooks module allows you to manage webhooks, subscriptions, and handle event notifications.

## Access

```python
# V1
client.webhooks.v1
```

## Webhooks V1

### Webhook Management

#### `create`
Create a new webhook endpoint.

```python
def create(self, payload_url: str, secret: str) -> Webhook
```

#### `list`
List all registered webhooks.

```python
def list(self, page: Optional[int] = 1, size: Optional[int] = 20) -> WebhookListResponse
```

#### `get`
Get details of a specific webhook.

```python
def get(self, webhook_id: str) -> Webhook
```

#### `update`
Update webhook details.

```python
def update(
    self, 
    webhook_id: str, 
    payload_url: Optional[str] = None, 
    secret: Optional[str] = None, 
    is_active: Optional[bool] = None
) -> Webhook
```

#### `delete`
Delete a webhook.

```python
def delete(self, webhook_id: str) -> None
```

### Signature Verification

#### `verify_signature`
Verify the signature of an incoming webhook request.

```python
def verify_signature(self, payload: str, headers: dict, secret: str) -> bool
```

### Events & Subscriptions

#### `list_events`
List all available event types.

```python
def list_events(self, page: Optional[int] = 1, size: Optional[int] = 20) -> EventListResponse
```

#### `subscribe`
Subscribe to an event.

```python
def subscribe(self, event_id: str, webhook_id: Optional[str] = None) -> Subscription
```

#### `update_subscription`
Update a subscription.

```python
def update_subscription(self, subscription_id: str, filter: Optional[dict] = None) -> Subscription
```

#### `unsubscribe`
Remove a subscription.

```python
def unsubscribe(self, subscription_id: str) -> None
```

#### `list_subscriptions`
List all active subscriptions.

```python
def list_subscriptions(self, page: Optional[int] = 1, size: Optional[int] = 20) -> SubscriptionListResponse
```

#### `get_subscription`
Get details of a subscription.

```python
def get_subscription(self, subscription_id: str) -> Subscription
```

### Notifications

#### `list_notifications`
List received notifications/events history.

```python
def list_notifications(self, page: Optional[int] = 1, size: Optional[int] = 20) -> NotificationListResponse
```

#### `request_sandbox_notification`
Trigger a fake notification for testing purposes (Sandbox only).

```python
def request_sandbox_notification(self, subscription_id: str) -> Notification
```
