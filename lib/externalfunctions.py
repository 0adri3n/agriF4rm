import random
import sqlite3
import string
import requests
import math

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))


def getwheatprice():
    
    url = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
    r = requests.get(url).json()
    price = math.floor(float(r["data"]["amount"])/100)/10
    return price

def getethprice():
    url = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
    r = requests.get(url).json()
    price = float(r["data"]["amount"])
    return price


def updaterenta(hashfield):

    conn = sqlite3.connect('data/field_database.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT dimension, basic_agri, rare_agri, epic_agri, legendary_agri FROM fieldsdetails WHERE hashfield=?""", (hashfield,))
    data = list(cursor.fetchone())

    renta = (data[1] + data[2]*1.5 + data[3]*2.5 + data[4]*4) * data[0]
    cursor.execute("""UPDATE fieldsdetails SET rentability = ? WHERE hashfield = ?""", (renta, hashfield))
    conn.commit()
    cursor.close()

