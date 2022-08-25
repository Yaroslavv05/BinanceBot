import time
from binance.client import Client
from tradingview_ta import TA_Handler, Interval
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class TradeFutures:

    def __init__(self, name_coin, leverage, col_vo_usdt, profit):
        self.__name_coin = name_coin
        self.__leverage = leverage
        self.__col_vo_usdt = col_vo_usdt
        self.__profit = profit

    def serch_indic(self):
        tesla = TA_Handler(
            symbol=self.__name_coin,
            screener="crypto",
            exchange='BINANCE',
            interval=Interval.INTERVAL_15_MINUTES)
        tesla_indic = tesla.get_indicators()
        self.indic_up_round = round(tesla_indic.get('BB.upper'), 4)
        self.indic_low_round = round(tesla_indic.get('BB.lower'), 4)
        print(self.indic_up_round)
        print(self.indic_low_round)

    def open_orders_futures_long(self):
        self.colvo_usdt_long = round((self.__col_vo_usdt * self.__leverage) / self.indic_up_round, 1)
        limit_order_long = client.futures_create_order(
            symbol=self.__name_coin,
            side='BUY',
            positionSide='LONG',
            type='LIMIT',
            quantity=self.colvo_usdt_long,
            timeInForce='GTC',
            price=self.indic_up_round)
        print(limit_order_long)

    def stop_price_long(self):
        stop_price_long_round = round(float((self.price_coin_round * self.__profit / 100 + self.price_coin_round)), 4)
        sell_stop_market_long = client.futures_create_order(
            symbol=self.__name_coin,
            side='SELL',
            type='TAKE_PROFIT_MARKET',
            positionSide='LONG',
            quantity=self.colvo_usdt_long,
            stopPrice=stop_price_long_round)
        print(sell_stop_market_long)

    def open_orders_futures_short(self):
        self.colvo_usdt_short = round((self.__col_vo_usdt * self.__leverage) / self.indic_low_round, 1)
        limit_order_short = client.futures_create_order(
            symbol=self.__name_coin,
            side='SELL',
            positionSide='SHORT',
            type='LIMIT',
            quantity=self.colvo_usdt_short,
            timeInForce='GTC',
            price=self.indic_low_round)
        print(limit_order_short)

    def stop_price_short(self):
        stop_price_short_round = round(float((self.price_coin_round * self.__col_vo_usdt / 100 - self.price_coin_round) * -1), 4)
        sell_stop_market_short = client.futures_create_order(
            symbol=self.__name_coin,
            side='SELL',
            type='TAKE_PROFIT_MARKET',
            positionSide='SHORT',
            quantity=self.colvo_usdt_short,
            stopPrice=stop_price_short_round)
        print(sell_stop_market_short)

    def do(self):
        while True:
            time.sleep(30)
            open_orders_futures = client.futures_get_open_orders()
            open_orders_futures_len = len(open_orders_futures)
            print(open_orders_futures_len)
            if open_orders_futures_len == 0:
                time.sleep(180)
                self.serch_indic()
                leverage = client.futures_change_leverage(symbol=self.__name_coin, leverage=self.__leverage)
                print(leverage)
                open_orders_futures = client.futures_get_open_orders()
                open_orders_futures_len = len(open_orders_futures)
                if open_orders_futures_len >= 0:
                    coin = client.get_symbol_ticker(symbol=self.__name_coin)
                    self.price_coin_round = round(float(coin.get('price')), 4)
                    if self.price_coin_round >= self.indic_up_round:
                        self.open_orders_futures_long()
                        self.stop_price_long()
                    if self.price_coin_round <= self.indic_low_round:
                        self.open_orders_futures_short()
                        self.stop_price_short()
                time.sleep(180)
            elif open_orders_futures_len > 0:
                print('Бот работает!')
            time.sleep(30)

