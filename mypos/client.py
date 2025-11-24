from .base import BaseClient
from .transactions.v1 import TransactionsV1
from .transactions.v1_1 import TransactionsV1_1
from .devices.v1 import DevicesV1
from .devices.v1_1 import DevicesV1_1
from .webhooks.v1 import WebhooksV1
from .webhooks.v1_1 import WebhooksV1_1
from .psd2.v1 import PSD2V1

class Transactions:
    def __init__(self, client):
        self.v1 = TransactionsV1(client)
        self.v1_1 = TransactionsV1_1(client)

class Devices:
    def __init__(self, client):
        self.v1 = DevicesV1(client)
        self.v1_1 = DevicesV1_1(client)

class Webhooks:
    def __init__(self, client):
        self.v1 = WebhooksV1(client)
        self.v1_1 = WebhooksV1_1(client)

class PSD2:
    def __init__(self, client):
        self.v1 = PSD2V1(client)

class MyPOS(BaseClient):
    """
    Main MyPOS Client.
    """
    def __init__(self):
        super().__init__()
        self.transactions = Transactions(self)
        self.devices = Devices(self)
        self.webhooks = Webhooks(self)
        self.psd2 = PSD2(self)
