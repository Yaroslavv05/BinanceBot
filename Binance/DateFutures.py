import sqlite3
from FururesBot import TradeFutures

class DateFutures:

    con = sqlite3.connect('Bot.db')
    cur = con.cursor()

    def __init__(self, user_ID, name_coin_futures, leverage, sum_usdt, profit):
        self.user_ID = user_ID
        self.name_coin_futures = name_coin_futures
        self.leverage = leverage
        self.sum_usdt = sum_usdt
        self.profit = profit

        try:
            self.cur.execute("CREATE TABLE trade(user_ID, name_coin_futures, leverage, sum_usdt, profit)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def isUserDatebase(self):
        data = self.cur.execute('SELECT * FROM trade')
        for i in data.fetchall():
            if self.user_ID == i[0]:
                return True
        return False

    def input_date(self):
        if not self.isUserDatebase():
            self.cur.execute(f'INSERT INTO trade VALUES (?, ?, ?, ?, ?)',
                             (self.user_ID, self.name_coin_futures, self.leverage, self.sum_usdt, self.profit))
            self.con.commit()

    def get_info(self):
        name_coin_futures = self.name_coin_futures
        leverage = self.leverage
        sum_usdt = self.sum_usdt
        profit = self.profit
        main = TradeFutures(name_coin_futures, leverage, sum_usdt, profit)
        main.do()

