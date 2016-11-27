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

def leaderboard():
    try:
        cursor.execute('SELECT userid, balance FROM chopbot ORDER BY balance DESC')
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(e)
        raise
        return False


def checkbalance(userid):
    try:
        cursor.execute('SELECT balance FROM chopbot WHERE userid=?', (userid,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO chopbot(userid, balance) VALUES(?,?)', (userid, 0))
            db.commit()
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
            amount = float(amount) + float(data[0])
            cursor.execute('UPDATE chopbot SET balance=? WHERE userid=?', (amount, userid))
            db.commit()
            return 'updatedbalance'
    except sqlite3.Error as e:
        print(e)
        raise
        return 'sqlerrorfromaddbalance'

def createlinkme():
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS linkme(name VARCHAR(140), text VARCHAR(140))')
        db.commit()
        print('Accessed table.')
        return True
    except sqlite3.Error as e:
        print(e)
        raise
        return False

def getlinkme(name):
    try:
        cursor.execute('SELECT balance FROM linkme WHERE name=?', (name,))
        data = cursor.fetchone()
        if data is None:
            return 'Error: Cannot find text.'
        return data
    except sqlite3.Error as e:
        print(e)
        raise
        return False

def addlinkme(name, text):
    try:
        data = checkbalance(name)
        if data is False:
            return 'sqlerrorfromchecklinkme'
        if data is None:
            cursor.execute('INSERT INTO linkme(name, text) VALUES(?,?)', (name, text))
            db.commit()
            return 'addedlinkme'
        else:
            cursor.execute('UPDATE chopbot SET text=? WHERE name=?', (text, name))
            db.commit()
            return 'updatedlinkme'
    except sqlite3.Error as e:
        print(e)
        raise
        return 'sqlerrorfromaddlinkme'

def checklinkme(name):
    try:
        cursor.execute('SELECT balance FROM linkme WHERE name=?', (name,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute('INSERT INTO linkme(name, text) VALUES(?,?)', (name, ''))
            db.commit()
            cursor.execute('SELECT balance FROM linkme WHERE name=?', (name,))
            data = cursor.fetchone()
        return data
    except sqlite3.Error as e:
        print(e)
        raise
        return False