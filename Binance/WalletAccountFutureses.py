from binance.client import Client
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class WalletFutures:

    def main(self):
        balance_futures = client.futures_account_balance()
        self.balance_futures_get = str(round(float(balance_futures[6].get('balance')), 2))