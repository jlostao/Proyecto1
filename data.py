import pymysql
import pymysql.cursors


con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)

cards = {}

try:
    with con.cursor() as cur:
        cur.execute('SELECT * FROM card')
        rows = cur.fetchall()
        for card in rows:
            cards[card["card_id"]] = {}
            cards[card["card_id"]]["value"] = card["card_value"]
            cards[card["card_id"]]["priority"] = card["card_priority"]
            cards[card["card_id"]]["realValue"] = card["card_real_value"]
finally:
    con.close()

players = {}

game = []

deck = []

roundPrint = {}