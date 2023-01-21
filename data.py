import pymysql
import pymysql.cursors

cards = {}

con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', 
      database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
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


players = {
"11115555A" :{"name":"Mario", "human":False, "bank":False, "initialCard":"", "priority":0, "type":30, "bet":0, "points":2, "cards":[], "roundPoints":0},
"22225555A" :{"name":"Pedro", "human":False, "bank":False, "initialCard":"", "priority":0, "type":40, "bet":0, "points":3, "cards":[], "roundPoints":0},
"32225555A" :{"name":"Maria", "human":True, "bank":False, "initialCard":"", "priority":0, "type":50, "bet":0, "points":4, "cards":[], "roundPoints":0}
}

game = ["11115555A", "22225555A", "32225555A"]

deck = []

roundPrint = {}