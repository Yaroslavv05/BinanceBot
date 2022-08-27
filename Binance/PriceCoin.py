from binance.client import Client
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class knowCoin:

    def __init__(self, name_coin):
        self.name_coin = name_coin

    def know(self):
        price_all = client.get_symbol_ticker(symbol=self.name_coin)
        self.price = str(float(price_all.get('price')))