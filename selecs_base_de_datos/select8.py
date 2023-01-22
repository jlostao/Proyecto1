import pymysql
import pymysql.cursors

avgbets={}
con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM',
      database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
try:
    with con.cursor() as cur:
        cur.execute('select cardgame_id as id de la partida, avg(bet_points) as apuesta media from player_game_round group by cardgame_id')
        rows=cur.fetchall()
        for bet in rows:
            avgbets[bet['cardgame_id']]={}
            avgbets[bet['cardgame_id']]['bet_points']= bet['bet']
            avgbets[bet['cardgame_id']]['cardgame_id']=bet['game']
finally:
    con.close

print(avgbets)