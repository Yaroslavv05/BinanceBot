from binance.client import Client
from Config import API_KEY, SECRET_KEY
import time

client = Client(API_KEY, SECRET_KEY)

class TradeCoin:

    def __init__(self, full_name_coin, name_coin, pair, colvo_coin, profit_spot, avg_time):
        self.__full_name_coin = full_name_coin
        self.__name_coin = name_coin
        self.__pair = pair
        self.__colvo_coin = colvo_coin
        self.__profit_spot = profit_spot
        self.avg_time = avg_time

    def open_orders_spot(self):
        buy_limit = client.create_order(
            symbol=self.__full_name_coin,
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',
            quantity=self.__colvo_coin,
            price=self.avg_price)
        print(buy_limit)
        coin_price_get = buy_limit.get('coin_price')
        self.price_per_buy.write(coin_price_get)

    def avg_price_5min(self):
        klines_5m = client.get_historical_klines(self.__full_name_coin, Client.KLINE_INTERVAL_5MINUTE, '1 day UTC')
        avg_5 = len(klines_5m) - 1
        self.b_5 = klines_5m[avg_5]
        self.avg_price = float(self.b_5[3])
        self.open_orders_spot()

    def avg_price_15min(self):
        klines_5m = client.get_historical_klines(self.__full_name_coin, Client.KLINE_INTERVAL_15MINUTE, '1 day UTC')
        avg_5 = len(klines_5m) - 1
        self.b_5 = klines_5m[avg_5]
        self.avg_price = float(self.b_5[3])
        self.open_orders_spot()

    def avg_price_60min(self):
        klines_5m = client.get_historical_klines(self.__full_name_coin, Client.KLINE_INTERVAL_1HOUR, '1 day UTC')
        avg_5 = len(klines_5m) - 1
        self.b_5 = klines_5m[avg_5]
        self.avg_price = float(self.b_5[3])
        self.open_orders_spot()

    def avg_price_240min(self):
        klines_5m = client.get_historical_klines(self.__full_name_coin, Client.KLINE_INTERVAL_4HOUR, '1 day UTC')
        avg_5 = len(klines_5m) - 1
        self.b_5 = klines_5m[avg_5]
        self.avg_price = float(self.b_5[3])
        self.open_orders_spot()


    def close_orders_spot(self):
        profit = float(round((self.avg_price * self.__profit_spot / 100) + self.avg_price), 2)
        sel_limit = client.create_order(
            symbol=self.__full_name_coin,
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=self.__colvo_coin,
            price=profit)
        price_on_sell = sel_limit.get('price')
        self.price_per_sell.write(price_on_sell)
        print(sel_limit)
        self.price_per_buy.close()
        self.price_per_sell.close()

    def do(self):
        time.sleep(60)
        self.price_per_buy = open('Цена за покупку.txt', 'w')
        self.price_per_sell = open('Цена за продажу.txt', 'w')
        if self.avg_price == '5 мин':
            self.avg_price_5min()
        elif self.avg_price == '15 мин':
            self.avg_price_15min()
        elif self.avg_price == '60 мин':
            self.avg_price_60min()
        elif self.avg_price == '240 мин':
            self.avg_price_240min()
        time.sleep(120)
        self.close_orders_spot()



