import pymysql
import pymysql.cursors

bank_players={}
con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM',
      database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
try:
    with con.cursor() as cur:
        cur.execute('select cardgame_id as id de la partida, count(distinct player_id) as Cantidad de usuarios siendo banca from player_game_round where is_bank=1 group by cardgame_id')
        rows=cur.fetchall()
        for bank in rows:
            bank_players[bank['cardgame_id']]={}
            bank_players[bank['cardgame_id']]['cardgame_id']= bank['game']
            bank_players[bank['cardgame_id']]['is_bank']= bank['player_bank']
finally:
    con.close

print(bank_players)
