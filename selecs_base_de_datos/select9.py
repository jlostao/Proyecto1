import pymysql
import pymysql.cursors

avg1Rbets={}
con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM',
      database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
try:
    with con.cursor() as cur:
        cur.execute('select cardgame_id as id de la partida, avg(bet_points) as apuesta media primera ronda from player_game_round where round_num=1 group by cardgame_id')
        rows=cur.fetchall()
        for bet1R in rows:
            avg1Rbets[bet1R['cardgame_id']]={}
            avg1Rbets[bet1R['cardgame_id']]['bet_points']= bet1R['bet_firstgame']
            avg1Rbets[bet1R['cardgame_id']]['cardgame_id']=bet1R['game']
finally:
    con.close

print(avg1Rbets)
