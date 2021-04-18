from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
import yaml
import pandas as pd
import time
import sys

with open(r'binance_secrets.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    binance_api = yaml.load(file, Loader=yaml.FullLoader)

client = Client(binance_api["api_key"], binance_api["api_secret"])

if client.get_system_status()["status"] != 0:
    print("Binance client is not available")
