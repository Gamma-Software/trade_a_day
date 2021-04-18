from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor
import yaml
import pandas as pd
import time
import sys

# TODO check if the currency to use needs to be converted if the pair is not

print("Buy me some cryptos / my P2P id: xxxxx")

with open(r'binance_secrets.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    binance_api = yaml.load(file, Loader=yaml.FullLoader)

pair = binance_api["currency_to_trade_with"] + binance_api["crypto_to_invest"]
test = True
client = Client(binance_api["api_key"], binance_api["api_secret"])

if client.get_system_status()["status"] != 0:
    print("Binance client is not available")

# get market depth
#depth = client.get_order_book(symbol=pair)

# TODO check if the trade is possible
#info = client.get_account_snapshot(type='SPOT')
#products = client.get_products()
#print(info)

price = {pair: pd.DataFrame(columns=['date', 'price']), 'error': False}


# check for it like so
def process_message(msg):
    if msg['e'] == 'error':
        # close and restart the socket
        print("e")
    else:
        print(msg["c"])


def pairs_trade(msg):
    """ define how to process incoming WebSocket messages """
    if msg['e'] != 'error':
        price[pair].loc[len(price[pair])] = [pd.Timestamp.now(), float(msg['c'])]
    else:
        price['error']: True


while True:
    # error check to make sure WebSocket is working
    if price['error']:
        # init and start the WebSocket
        bsm = BinanceSocketManager(client)
        conn_key = bsm.start_symbol_ticker_socket(pair, pairs_trade)
        bsm.start()
        price['error'] = False
    else:
        df = price[pair]
        start_time = df.date.iloc[-1] - pd.Timedelta(minutes=5)
        df = df.loc[df.date >= start_time]
        max_price = df.price.max()
        min_price = df.price.min()

        if df.price.iloc[-1] < max_price * (1-binance_api["down_change_percent"]*0.01):
            try:
                if test:
                    order = client.create_test_order(symbol=pair, quantity=binance_api["daily_amount"])
                else:
                    order = client.order_market_buy(symbol=pair, quantity=binance_api["daily_amount"])
                break
            except BinanceAPIException as e:
                # error handling goes here
                print(e)
            except BinanceOrderException as e:
                # error handling goes here
                print(e)

    time.sleep(0.1)

# Stop the web socket
bsm.stop_socket(conn_key)
reactor.stop()
