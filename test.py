from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor
import yaml
import pandas as pd
import time
import sys


with open(r'binance_secrets.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    binance_api = yaml.load(file, Loader=yaml.FullLoader)


def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something


client = Client(binance_api["api_key"], binance_api["api_secret"])


bm = BinanceSocketManager(client)
# start any sockets here, i.e a trade socket
conn_key = bm.start_trade_socket('BNBBTC', process_message)
# then start the socket manager
bm.start()
