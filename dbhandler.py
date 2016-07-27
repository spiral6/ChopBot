import sqlite3



def connect():
    try:
        global db
        global cursor
        db = sqlite3.connect("chopbot.db")
        cursor = db.cursor()
        print('Connected to database.')
        return True
    except sqlite3.Error as e:
        print(e)
        raise
        return False


def create():
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS chopbot(userid INTEGER, balance REAL)')
        db.commit()
        print('Accessed table.')
        return True
    except sqlite3.Error as e:
        print(e)
        raise
        return False


def checkbalance(userid):
    try:
        cursor.execute('SELECT balance FROM chopbot WHERE userid=?', (userid,))
        data = cursor.fetchone()
        return data
    except sqlite3.Error as e:
        print(e)
        raise
        return False


def addbalance(userid, amount):
    try:
        data = checkbalance(userid)
        if data is False:
            return 'sqlerrorfromcheckbalance'
        if data is None:
            cursor.execute('INSERT INTO chopbot(userid, balance) VALUES(?,?)', (userid, amount))
            db.commit()
            return 'addeduserandbalance'
        else:
            amount = amount + data[0]
            cursor.execute('UPDATE chopbot SET balance=? WHERE userid=?', (amount, userid))
            db.commit()
            return 'updatedbalance'
    except sqlite3.Error as e:
        print(e)
        raise
        return 'sqlerrorfromaddbalance'
