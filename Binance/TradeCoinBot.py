from binance.client import Client
from Config import API_KEY, SECRET_KEY
import time

client = Client(API_KEY, SECRET_KEY)

class TradeCoin:

    def __init__(self, full_name_coin, name_coin, pair, colvo_coin, profit_spot):
        self.__full_name_coin = full_name_coin
        self.__name_coin = name_coin
        self.__pair = pair
        self.__colvo_coin = colvo_coin
        self.__profit_spot = profit_spot

    def open_orders_spot(self):
        balance = client.get_asset_balance(asset=self.__pair)
        self.free_balance = float(balance.get('free'))
        klines_5m = client.get_historical_klines(self.__full_name_coin, Client.KLINE_INTERVAL_5MINUTE, '1 day UTC')
        avg_5 = len(klines_5m) - 1
        self.b_5 = klines_5m[avg_5]
        buy_limit = client.create_order(
            symbol=self.__full_name_coin,
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',
            quantity=self.__colvo_coin,
            price=self.avg_price)
        coin_price = float(buy_limit.get('price'))
        coin_price_get = buy_limit.get('coin_price')
        print(buy_limit)
        print(coin_price)
        self.price_per_buy.write(coin_price_get)
        time.sleep(5)
        print(self.avg_price)


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
        time.sleep(1)
        self.price_per_buy = open('Цена за покупку.txt', 'w')
        self.price_per_sell = open('Цена за продажу.txt', 'w')
        self.avg_price = float(self.b_5[3])
        if self.free_balance >= 10:
            self.open_orders_spot()
            self.close_orders_spot()


main = TradeCoin(input('Введите полное название монетки ->').upper(), input('Введите название монеток ->').upper(), input('Введите пару монетки ->').upper(), float(input('Введите кол-во монет ->')), float(input('Введите какой профит хотите получить ->')))
main.do()


