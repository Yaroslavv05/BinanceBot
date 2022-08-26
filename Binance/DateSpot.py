import sqlite3
from TradeCoinBot import TradeCoin

class DateSpot:

    con = sqlite3.connect('Bot.db')
    cur = con.cursor()

    def __init__(self, user_ID, full_name_coin, name_coin, pair, colvo_coin, profit, avg_time):
        self.user_ID = user_ID
        self.full_name_coin = full_name_coin
        self.name_coim = name_coin
        self.pair = pair
        self.colvo_coin = colvo_coin
        self.profit = profit
        self.avg_time = avg_time

        try:
            self.cur.execute("CREATE TABLE trade_spot(user_ID, full_name_coin, name_coin, pair, colvo_coin, profit, avg_time)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass


    def isUserDateBase(self):
        data = self.cur.execute('SELECT * FROM trade_spot')
        for i in data.fetchall():
            if self.user_ID == i[0]:
                return True
        return False

    def input_date(self):
        if not self.isUserDateBase():
            self.cur.execute(f'INSERT INTO trade_spot VALUES (?, ?, ?, ?, ?, ?, ?)',
                             (self.user_ID, self.full_name_coin, self.name_coim, self.pair, self.colvo_coin, self.profit, self.avg_time))
            self.con.commit()

    def get_info(self):
       full_name_coin = self.full_name_coin
       name_coin = self.name_coim
       pair = self.pair
       colvo_coin = self.colvo_coin
       profit = self.profit
       avg_time = self.avg_time
       main = TradeCoin(full_name_coin, name_coin, pair, colvo_coin, profit, avg_time)
       main.do()
