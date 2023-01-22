import pymysql
import pymysql.cursors

avgLRbets={}
con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM',
      database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
try:
    with con.cursor() as cur:
        cur.execute('select pr.cardgame_id as id de la partida, avg(pr.bet_points) as apuesta media ultima ronda from player_game_round pr inner join cardgame c on c.cardgame_id=pr.cardgame_id where round_num=rounds group by pr.cardgame_id')
        rows=cur.fetchall()
        for betLR in rows:
            avg1Rbets[betLR['cardgame_id']]={}
            avg1Rbets[betLR['cardgame_id']]['bet_points']= betLR['bet_lastgame']
            avg1Rbets[betLR['cardgame_id']]['cardgame_id']=betLR['game']
finally:
    con.close

print(avgLRbets)