from .client import MyPOS
from .schemas import *

def create_client() -> MyPOS:
    return MyPOS()



def create_client() -> Client:
    mypos_client: Client = Client()
    return mypos_client