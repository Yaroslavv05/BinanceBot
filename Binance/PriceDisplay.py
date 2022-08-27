from binance.client import Client
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class Display:

    def __init__(self, name_coin):
        self.name_coin = name_coin

    def display(self):
        price_5m = open('../Цены за 5 мин.txt', 'w')
        price_15m = open('../Цены за 15 мин.txt', 'w')
        self.price_5m_r = open('../Цены за 5 мин.txt', 'rb')
        self.price_15m_r = open('../Цены за 15 мин.txt', 'rb')
        klines_5m = client.get_historical_klines(self.name_coin, Client.KLINE_INTERVAL_5MINUTE, '1 day UTC')
        for i in range(len(klines_5m)):
            a_5 = klines_5m[i]
            price_5m.write(str(float(a_5[3])) + ' $' + '\n')
        klines_15m = client.get_historical_klines(self.name_coin, Client.KLINE_INTERVAL_15MINUTE, '1 day UTC')
        for i in range(len(klines_15m)):
            a_15 = klines_15m[i]
            price_15m.write(str(float(a_15[3])) + ' $' + '\n')
        price_5m.close()
        price_15m.close()