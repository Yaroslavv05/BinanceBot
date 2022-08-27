from binance.client import Client
from Config import API_KEY, SECRET_KEY

client = Client(API_KEY, SECRET_KEY)

class walet:

    def main(self):
        assets_ada = client.get_asset_balance(asset='ADA')
        self.ada_balance = assets_ada.get('free')
        assets_bnb = client.get_asset_balance(asset='BNB')
        self.bnb_balance = assets_bnb.get('free')
        assets_xrp = client.get_asset_balance(asset='XRP')
        self.xrp_balance = assets_xrp.get('free')
        assets_usdt = client.get_asset_balance(asset='USDT')
        self.usdt_balance = assets_usdt.get('free')
        ada_price = client.get_symbol_ticker(symbol='ADAUSDT')
        self.symvol = ada_price.get('symbol')
        self.price = ada_price.get('price')
        bnb_price = client.get_symbol_ticker(symbol='BNBUSDT')
        self.b_price = bnb_price.get('price')
        xrp_price = client.get_symbol_ticker(symbol='XRPUSDT')
        self.x_price = xrp_price.get('price')