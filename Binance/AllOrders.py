from binance.client import Client
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class Orsers:

    def __init__(self, name_coin):
        self.name_coin = name_coin

    def main(self):
        order = client.get_all_orders(symbol=self.name_coin)
        element_count = len([item for item in order])
        for i in range(element_count):
            self.order_symbol = order[i].get('symbol')
            self.order_price = order[i].get('price')
            self.order_origQty = order[i].get('origQty')
            self.order_cummulativeQuoteQty = order[i].get('cummulativeQuoteQty')
            self.order_side = order[i].get('side')