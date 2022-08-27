import sqlite3

class DateUsers:

    con = sqlite3.connect('Bot.db')
    cur = con.cursor()

    def __init__(self, user_id, name_user, full_name_user):
        self.user_id = user_id
        self.name_user = name_user
        self.full_name_user = full_name_user
        try:
            self.cur.execute("CREATE TABLE users(user_ID, name_user, full_name_user)")
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def isUserDatebase(self):
        data = self.cur.execute('SELECT * FROM users')
        for i in data.fetchall():
            if self.user_id == i[0]:
                return True
        return False

    def recorde_in_date(self):
        if not self.isUserDatebase():
            self.cur.execute(f'INSERT INTO users VALUES (?, ?, ?)',
                             (self.user_id, self.name_user, self.full_name_user))
            self.con.commit()

