import data
import pyfiglet
import os
import random
import pymysql
import pymysql.cursors
from datetime import datetime


def menuFunct(bannerText, menuText, menuInput, options):
    width = os.get_terminal_size().columns
    print("*" * width + "\n")
    print(pyfiglet.figlet_format(bannerText))
    print("\n" + "*" * width + "\n")
    print(menuText) 
    while True:
        try:
            result = input("\n" + menuInput) 
            for value in options: 
                if str(value) == result:
                    return int(result)  
            raise ValueError 
        except ValueError:
            print("The given value is not valid. Select one of the shown options.")


def setGameCards(deck):
    data.deck = []
    for card in data.cards:
        if deck == 1:
            if card[0] == "O" or card[0] == "E" or card[0] == "C" or card[0] == "B":
                data.deck.append(card)
                
        elif deck == 2:
            if card[0] == "H" or card[0] == "D" or card[0] == "T" or card[0] == "P":
                data.deck.append(card)
    

def resetPoints():
    for player in data.game:
        data.players[player]["points"] = 20   


def checkPlayersRange():
    if len(data.game) < 2 or len(data.game) > 6:
        return False
    else:
        return True


def check2PlayersWithPoints():
    playersalive = 0
    for player in data.game:
        if data.players[player]["points"] > 0:
            playersalive += 1
    if playersalive >= 2:
        return True
    else:
        return False


def setGamePriority():
    for player in data.game:
        cardposition = random.randint(0, len(data.deck) - 1)
        data.players[player]["initialCard"] = data.deck[cardposition]
        del data.deck[cardposition]
    for i in range(0, len(data.game)):
        a = 1
        for j in range(0, len(data.game)-(i+1)):
            if data.cards[data.players[data.game[j]]["initialCard"]]["realValue"] == data.cards[data.players[data.game[a]]["initialCard"]]["realValue"]:
                if data.cards[data.players[data.game[j]]["initialCard"]]["priority"] < data.cards[data.players[data.game[a]]["initialCard"]]["priority"]:
                    data.game[j], data.game[a] = data.game[a], data.game[j]
            elif data.cards[data.players[data.game[j]]["initialCard"]]["realValue"] < data.cards[data.players[data.game[a]]["initialCard"]]["realValue"]:
                data.game[j], data.game[a] = data.game[a], data.game[j]
            a += 1
    for i in range(0, len(data.game)):
        data.players[data.game[i]]["priority"] = len(data.game) - i
    for player in data.game:
        maxprio = len(data.game)
        if data.players[player]["priority"] == maxprio:
            data.players[player]["bank"] = True
    
    
    
def setBets():
    for player in data.game:
        if data.players[player]["bank"] is False:
            if data.players[player]["points"] <= 3:
                data.players[player]["bet"] = data.players[player]["points"]
            elif (data.players[player]["points"] * data.players[player]["type"]) / 100 <= 3:
                data.players[player]["bet"] = 3
            else:
                data.players[player]["bet"] = int((data.players[player]["points"] * data.players[player]["type"]) / 100)


def standarRound(id):
    while True:
        position = random.randint(0, len(data.deck) - 1)
        card = data.deck[position]
        data.players[id]["cards"].append(card)
        data.players[id]["roundPoints"] += data.cards[card]["value"]
        del data.deck[position]
        above = 0
        for card in data.deck:
            if data.cards[card]["value"] + data.players[id]["roundPoints"] > 7.5:
                above += 1
        if (above/len(data.deck)) * 100 > data.players[id]["type"]:
            break


def humanRound(id, round):
    while True and data.players[id]["roundPoints"] < 7.5:
        sel = menuFunct("Turn of " + data.players[id]["name"], "1)View Stats \n2)View Game Stats \n3)Set Bet \n4)Order Card \n5)Automatic Play \n6)Stand", "Option: ", [1,2,3,4,5,6])
        if sel == 1:
            width = os.get_terminal_size().columns
            print("*" * width + "\n")
            print(pyfiglet.figlet_format("Player Stats"))
            print("\n" + "*" * width + "\n")
            print("Name".ljust(14) + data.players[id]["name"] + "\nType".ljust(15) + str(data.players[id]["type"]) + "\nHuman".ljust(15) + str(data.players[id]["human"]) + 
                  "\nBank".ljust(15) + str(data.players[id]["bank"]) + "\nInitialCard".ljust(15) + data.players[id]["initialCard"] + "\nPriority".ljust(15) + str(data.players[id]["priority"]) + 
                  "\nBet".ljust(15) + str(data.players[id]["bet"]) + "\nPoints".ljust(15) + str(data.players[id]["points"]) + "\nCards".ljust(15) + str(data.players[id]["cards"]) + "\nRoundPoints".ljust(15) + str(data.players[id]["roundPoints"]))
            input("\nEnter to continue\n")
        elif sel == 2:
            printStats(id, round, True)
        elif sel == 3:
            while True:
                newBet = input("Set the new bet: ")
                if newBet.isdigit():
                    newBet = int(newBet)
                    if newBet >= 3 and newBet <= data.players[id]["points"]:
                        data.players[id]["bet"] = newBet
                        input("\nEnter to continue\n")
                        break
                    else:
                        print("The Bet range has to be between 3 and the max points of the user.")
                else:
                    print("The bet value must be an intenger number.")
                input("\nEnter to continue\n")
        elif sel == 4:
            if len(data.players[id]["cards"]) == 0:
                position = random.randint(0, len(data.deck) - 1)
                card = data.deck[position]
                data.players[id]["cards"].append(card)
                data.players[id]["roundPoints"] += data.cards[card]["value"]
                del data.deck[position]
                print("The new card is " + card + "\nNow you have " + str(data.players[id]["roundPoints"]) + " points")
                input("\nEnter to continue\n")
            else:
                above = 0
                for card in data.deck:
                    if data.cards[card]["value"] + data.players[id]["roundPoints"] > 7.5:
                        above += 1
                exceedChance = (above/len(data.deck) * 100)
                print("Chance of exceed 7.5: " + str(exceedChance) + "%")
                ordercard = input("Are you sure you want to order another card? Y/y = yes | Other key = no: ")
                if ordercard.lower() == "y":
                    position = random.randint(0, len(data.deck) - 1)
                    card = data.deck[position]
                    data.players[id]["cards"].append(card)
                    data.players[id]["roundPoints"] += data.cards[card]["value"]
                    del data.deck[position]
                    print("The new card is " + card + "\nNow you have " + str(data.players[id]["roundPoints"]) + " points")
                    input("\nEnter to continue\n")
        elif sel == 5:
            standarRound(id)
            break
        elif sel == 6:
            break


def bootBankRound(id):
    while True:
        position = random.randint(0, len(data.deck) - 1)
        card = data.deck[position]
        data.players[id]["cards"].append(card)
        data.players[id]["roundPoints"] += data.cards[card]["value"]
        del data.deck[position]
        wonPoints = 0
        lostPoints = 0
        playersPassed = 0
        for player in data.game:
            if data.players[player]["bank"] is False:
                if data.players[player]["roundPoints"] > 7.5:
                    playersPassed += 1
                    wonPoints += data.players[player]["bet"]
                elif data.players[player]["roundPoints"] <= data.players[id]["roundPoints"]:
                    playersPassed += 1
                    wonPoints += data.players[player]["bet"]
                elif data.players[player]["roundPoints"] > data.players[id]["roundPoints"] and data.players[player]["roundPoints"] == 7.5:
                    lostPoints += (data.players[player]["bet"] * 2)
                elif data.players[player]["roundPoints"] > data.players[id]["roundPoints"]:
                    lostPoints += data.players[player]["bet"]
        pointsDiff = lostPoints - wonPoints
        aboveCard = 0
        for card in data.deck:
            if data.cards[card]["value"] + data.players[id]["roundPoints"] > 7.5:
                aboveCard += 1
        if data.players[id]["roundPoints"] > 7.5 or data.players[id]["roundPoints"] == 7.5:
            break
        elif playersPassed == len(data.game) - 1:
            break
        elif playersPassed > 0 and pointsDiff < data.players[id]["points"] and aboveCard/len(data.deck) * 100 > data.players[id]["type"]:
            break
    

def humanBankRound(id, round):
    while True and data.players[id]["roundPoints"] < 7.5:
        sel = menuFunct("Turn of " + data.players[id]["name"], "1)View Stats \n2)View Game Stats \n3)Set Bet \n4)Order Card \n5)Automatic Play \n6)Stand", "Option: ", [1,2,3,4,5,6])
        if sel == 1:
            width = os.get_terminal_size().columns
            print("*" * width + "\n")
            print(pyfiglet.figlet_format("Player Stats"))
            print("\n" + "*" * width + "\n")
            print("Name".ljust(14) + data.players[id]["name"] + "\nType".ljust(15) + str(data.players[id]["type"]) + "\nHuman".ljust(15) + str(data.players[id]["human"]) + 
                  "\nBank".ljust(15) + str(data.players[id]["bank"]) + "\nInitialCard".ljust(15) + data.players[id]["initialCard"] + "\nPriority".ljust(15) + str(data.players[id]["priority"]) + 
                  "\nBet".ljust(15) + str(data.players[id]["bet"]) + "\nPoints".ljust(15) + str(data.players[id]["points"]) + "\nCards".ljust(15) + str(data.players[id]["cards"]) + "\nRoundPoints".ljust(15) + str(data.players[id]["roundPoints"]))
            input("\nEnter to continue\n")
        elif sel == 2:
            printStats(id, round, True)
        elif sel == 3:
            print("The Bank is not allowed to bet")
        elif sel == 4:
            if len(data.players[id]["cards"]) == 0:
                position = random.randint(0, len(data.deck) - 1)
                card = data.deck[position]
                data.players[id]["cards"].append(card)
                data.players[id]["roundPoints"] += data.cards[card]["value"]
                del data.deck[position]
                print("The new card is " + card + "\nNow you have " + str(data.players[id]["roundPoints"]) + " points")
                input("\nEnter to continue\n")
            else:
                above = 0
                for card in data.deck:
                    if data.cards[card]["value"] + data.players[id]["roundPoints"] > 7.5:
                        above += 1
                exceedChance = (above/len(data.deck) * 100)
                print("Chance of exceed 7.5: " + str(exceedChance) + "%")
                ordercard = input("Are you sure you want to order another card? Y/y = yes | Other key = no: ")
                if ordercard.lower() == "y":
                    position = random.randint(0, len(data.deck) - 1)
                    card = data.deck[position]
                    data.players[id]["cards"].append(card)
                    data.players[id]["roundPoints"] += data.cards[card]["value"]
                    del data.deck[position]
                    print("The new card is " + card + "\nNow you have " + str(data.players[id]["roundPoints"]) + " points")
                    input("\nEnter to continue\n")
        elif sel == 5:
            standarRound(id)
            break
        elif sel == 6:
            break


def distributionPointAndNewBankCandidates():
    bankCandidate = []
    for player in data.game:
        if data.players[player]["bank"] is True:
            bankID = player
        elif data.players[player]["bank"] is False:
            if data.players[bankID]["roundPoints"] == 7.5:
                data.players[player]["points"] -= data.players[player]["bet"]
                data.players[bankID]["points"] += data.players[player]["bet"]
            elif data.players[player]["roundPoints"] > 7.5 and data.players[bankID]["roundPoints"] < 7.5:
                data.players[player]["points"] -= data.players[player]["bet"]
                data.players[bankID]["points"] += data.players[player]["bet"]
            elif data.players[bankID]["roundPoints"] < 7.5 and data.players[bankID]["roundPoints"] >= data.players[player]["roundPoints"]:
                data.players[player]["points"] -= data.players[player]["bet"]
                data.players[bankID]["points"] += data.players[player]["bet"]
            elif data.players[player]["roundPoints"] == 7.5 and data.players[bankID]["roundPoints"] != 7.5:
                data.players[bankID]["points"] -= data.players[player]["bet"] * 2
                data.players[player]["points"] += data.players[player]["bet"] * 2
                bankCandidate.append(player)
            elif data.players[player]["roundPoints"] < 7.5 and data.players[player]["roundPoints"] > data.players[bankID]["roundPoints"]:
                data.players[bankID]["points"] -= data.players[player]["bet"] 
                data.players[player]["points"] += data.players[player]["bet"] 
            elif data.players[player]["roundPoints"] < 7.5 and data.players[bankID]["roundPoints"] > 7.5:
                data.players[bankID]["points"] -= data.players[player]["bet"] 
                data.players[player]["points"] += data.players[player]["bet"]
    for player in data.game:
        if data.players[player]["bank"] is False:
            if data.players[player]["points"] <= 0:
                data.game.remove(player)
    for player in data.game:
        if data.players[player]["bank"] is False:
            if data.players[player]["points"] <= 0:
                data.game.remove(player)
    for player in data.game:
        if data.players[player]["bank"] is True and data.players[player]["points"] <= 0:
            data.players[player]["bank"] = False
            data.game.remove(player)
            data.players[data.game[0]]["bank"] = True
            data.players[data.game[0]]["bet"] = 0
    if bankCandidate != []:
        for player in data.game:
            if data.players[player]["bank"] is True:
                data.players[player]["bank"] = False
        newBank = bankCandidate[random.randint(0, len(bankCandidate) - 1)]
        data.players[newBank]["bank"] = True
        data.players[newBank]["bet"] = 0
    

def printStats(id, curround, human):
    if human is True:
        print("*"*25 + " Round " + str(curround) + ", Turn of " + data.players[id]["name"] + " " + "*"*25 + "\n")
        print(data.roundPrint["name"])
        print(data.roundPrint["human"])
        print(data.roundPrint["priority"])
        print(data.roundPrint["type"])
        print(data.roundPrint["bank"])
        print(data.roundPrint["bet"])
        print(data.roundPrint["points"])
        print(data.roundPrint["cards"])
        print(data.roundPrint["roundpoints"])
        input("\nEnter to continue\n")
    elif id == "a":
        for i in range(len(data.game) - 1, -1, -1):
            data.roundPrint["name"] += data.players[data.game[i]]["name"].ljust(30)
            data.roundPrint["human"] += str(data.players[data.game[i]]["human"]).ljust(30)
            data.roundPrint["priority"] += str(data.players[data.game[i]]["priority"]).ljust(30)
            data.roundPrint["type"] += str(data.players[data.game[i]]["type"]).ljust(30)
            data.roundPrint["bank"] += str(data.players[data.game[i]]["bank"]).ljust(30)
            data.roundPrint["bet"] += str(data.players[data.game[i]]["bet"]).ljust(30)
            data.roundPrint["points"] += str(data.players[data.game[i]]["points"]).ljust(30)
    elif id == "b":
        data.roundPrint = {"name":"Name".ljust(20), "human":"Human".ljust(20), "priority":"Priority".ljust(20), "type":"Type".ljust(20), "bank":"Bank".ljust(20), 
                           "bet":"Bet".ljust(20), "points":"Points".ljust(20), "cards":"Cards".ljust(20), "roundpoints":"Roundpoints".ljust(20)}
        for i in range(len(data.game) - 1, -1, -1):
            data.roundPrint["name"] += data.players[data.game[i]]["name"].ljust(30)
            data.roundPrint["human"] += str(data.players[data.game[i]]["human"]).ljust(30)
            data.roundPrint["priority"] += str(data.players[data.game[i]]["priority"]).ljust(30)
            data.roundPrint["type"] += str(data.players[data.game[i]]["type"]).ljust(30)
            data.roundPrint["bank"] += str(data.players[data.game[i]]["bank"]).ljust(30)
            data.roundPrint["bet"] += str(data.players[data.game[i]]["bet"]).ljust(30)
            data.roundPrint["points"] += str(data.players[data.game[i]]["points"]).ljust(30)
            cards = ""
            for card in data.players[data.game[i]]["cards"]:
                cards += card + ";"
            data.roundPrint["cards"] += cards.ljust(30)
            data.roundPrint["roundpoints"] += str(data.players[data.game[i]]["roundPoints"]).ljust(30)
        print("*"*25 + " Round results " + "*"*25 + "\n")
        print(data.roundPrint["name"])
        print(data.roundPrint["human"])
        print(data.roundPrint["priority"])
        print(data.roundPrint["type"])
        print(data.roundPrint["bank"])
        print(data.roundPrint["bet"])
        print(data.roundPrint["points"])
        print(data.roundPrint["cards"])
        print(data.roundPrint["roundpoints"])
        input("\nEnter to continue\n")
    else:
        cards = ""
        for card in data.players[id]["cards"]:
            cards += card + ";"
        data.roundPrint["cards"] += cards.ljust(30)
        data.roundPrint["roundpoints"] += str(data.players[id]["roundPoints"]).ljust(30)
        print("*"*25 + " Round " + str(curround) + ", Turn of " + data.players[id]["name"] + " " + "*"*25 + "\n")
        print(data.roundPrint["name"])
        print(data.roundPrint["human"])
        print(data.roundPrint["priority"])
        print(data.roundPrint["type"])
        print(data.roundPrint["bank"])
        print(data.roundPrint["bet"])
        print(data.roundPrint["points"])
        print(data.roundPrint["cards"])
        print(data.roundPrint["roundpoints"])
        input("\nEnter to continue\n")
    

def resetStats():
    for player in data.game:
        data.players[player]["cards"] = []
        data.players[player]["roundPoints"] = 0


def orderPlayersByPriority():
    for player in data.game:
        if data.players[player]["bank"] is True:
            bank = [player]
            data.game.remove(player)
    for i in range(0, len(data.game)):
        a = 1
        for j in range(0, len(data.game)-(i+1)):
            if data.players[data.game[j]]["priority"] < data.players[data.game[a]]["priority"]:
                data.game[j], data.game[a] = data.game[a], data.game[j]
            a += 1
    players = bank + data.game
    data.game = players
    

def printWinner(curround):
    if check2PlayersWithPoints():
        for i in range(0, len(data.game)):
            a = 1
            for j in range(0, len(data.game)-(i+1)):
                if data.players[data.game[j]]["points"] == data.players[data.game[a]]["points"]:
                    if data.players[data.game[j]]["priority"] < data.players[data.game[a]]["priority"]:
                        data.game[j], data.game[a] = data.game[a], data.game[j]
                else:
                    if data.players[data.game[j]]["points"] < data.players[data.game[a]]["points"]:
                        data.game[j], data.game[a] = data.game[a], data.game[j]
                a += 1
        width = os.get_terminal_size().columns
        print("*" * width + "\n")
        print(pyfiglet.figlet_format("Game Over"))
        print("\n" + "*" * width + "\n")
        print("The winner is " + data.game[0] + " - " + data.players[data.game[0]]["name"] + ", in " + str(curround - 1) + 
              " rounds, with " + str(data.players[data.game[0]]["points"]) + " points")
    else:
        print("The winner is " + data.game[0] + " - " + data.players[data.game[0]]["name"] + ", in " + str(curround - 1) + 
              " rounds, with " + str(data.players[data.game[0]]["points"]) + " points")
    input("\nEnter to continue\n")


def playGame(round, deck):
    setGamePriority()
    resetPoints()
    data.cardgame = {}
    data.player_game = {}
    data.player_round_game = {}
    curtime = datetime.now()
    curtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
    try:
        totalcardgame = []
        with con.cursor() as cur:
            cur.execute("SELECT cardgame_id FROM cardgame")
            rows = cur.fetchall()
            for id in rows:
                totalcardgame.append(id)
    finally:
        con.close()
    data.cardgame = {"cardgame_id":len(totalcardgame) + 1, "players":len(data.game), "rounds":0, "start_hour":curtime, "end_hour":"", "deck_id":deck}
    data.player_game[len(totalcardgame) + 1] = {}
    for player in data.game:
        data.player_game[len(totalcardgame) + 1][player] = {"initial_card_id":data.players[player]["initialCard"], "starting_points":data.players[player]["points"], "ending_points":0}
    data.player_round_game[len(totalcardgame) + 1] = {}
    for i in range(round):
        data.player_round_game[len(totalcardgame) + 1][i+1] = {}
        for player in data.game:
            data.player_round_game[len(totalcardgame) + 1][i+1][player] = {"is_bank":data.players[player]["bank"], "bet_points":0, "starting_round_points":20, "cards_value":0, "ending_round_points":0}
    currentround = 1
    while round > 0 and check2PlayersWithPoints():
        data.roundPrint = {"name":"Name".ljust(20), "human":"Human".ljust(20), "priority":"Priority".ljust(20), "type":"Type".ljust(20), "bank":"Bank".ljust(20), 
                           "bet":"Bet".ljust(20), "points":"Points".ljust(20), "cards":"Cards".ljust(20), "roundpoints":"Roundpoints".ljust(20)}
        setGameCards(deck)
        setBets()
        for player in data.game:
            data.player_round_game[len(totalcardgame) + 1][currentround][player]["starting_round_points"] = data.players[player]["points"]
            data.player_round_game[len(totalcardgame) + 1][currentround][player]["is_bank"] = data.players[player]["bank"]
            data.player_round_game[len(totalcardgame) + 1][currentround][player]["bet_points"] = data.players[player]["bet"]
        printStats("a", currentround, False)
        for i in range(len(data.game) - 1, -1, -1):
            if data.players[data.game[i]]["bank"] is False:
                if data.players[data.game[i]]["human"] is True:
                    humanRound(data.game[i], currentround)
                elif data.players[data.game[i]]["human"] is False:
                    standarRound(data.game[i])
                printStats(data.game[i], currentround, False)
        for player in data.game:
            if data.players[player]["bank"] is True:
                if data.players[data.game[i]]["human"] is True:
                    humanBankRound(data.game[i], currentround)
                elif data.players[data.game[i]]["human"] is False:
                    bootBankRound(player)
                printStats(player, currentround, False)
        distributionPointAndNewBankCandidates()
        printStats("b", round, False)
        for player in data.game:
            data.player_round_game[len(totalcardgame) + 1][currentround][player]["cards_value"] = data.players[player]["roundPoints"]
            data.player_round_game[len(totalcardgame) + 1][currentround][player]["ending_round_points"] = data.players[player]["points"]
        orderPlayersByPriority()
        resetStats()
        currentround += 1
        round -= 1
    curtime = datetime.now()
    curtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    data.cardgame["rounds"] = currentround -1
    data.cardgame["end_hour"] = curtime
    for player in data.game:
        data.player_game[len(totalcardgame) + 1][player]["ending_points"] = data.players[player]["points"]
    sendCardgame(data.cardgame)
    sendPlayer_game(data.player_game)
    sendPlayer_round_game(data.player_round_game)
    printWinner(currentround)


def allPlayersID():
    playersID = []
    con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT player_id FROM player')
            pid = cur.fetchall()
            for id in pid:
                playersID.append(id)
    finally:
        con.close()
    return playersID


def newHuman():
    width = os.get_terminal_size().columns
    print("*" * width + "\n")
    print(pyfiglet.figlet_format("New Bot Player"))
    print("\n" + "*" * width + "\n")
    while True:
        newName = input("Name: ")
        if newName.isalnum() is False:
            print("\nIncorrect name. The name introduced must only contain letters and numbers and not have spaces.\n")
            input("\nEnter to continue\n")
        else:
            break
    print("\nName:".ljust(10) + newName)
    while True:
        nifletter = "TRWAGMYFPDXBNJZSQVHLCKE"
        newNif = input("NIF: ")
        if len(newNif) != 9:
            print("Incorrect NIF format")
            input("\nEnter to continue\n")
        else:
            if newNif[0:8].isdigit() is False or newNif[8].isalpha() is False:
                print("\nIncorrect NIF format")
                input("\nEnter to continue\n")
            else:
                if nifletter[int(newNif[0:8])%23] != newNif[8].upper():
                    print("\nIncorrect NIF letter")
                    input("\nEnter to continue\n")
                else:
                    exist = False
                    playersID = allPlayersID()
                    for id in playersID:
                        if id[0] == newNif:
                            exist = True
                    if exist:
                        print("\nNIF already exists")
                        input("\nEnter to continue\n")
                    else:
                        break   
    print("\nName:".ljust(10) + newName + "\nDNI:".ljust(10) + newNif)
    while True:
        newType = input("\nSelect profile for the new boot: \n1)Cautious \n2)Moderated \n3)Bold \nOption: ")
        options = [1, 2, 3]
        exist = False
        for value in options: 
            if str(value) == newType:
                exist = True
                newType = int(newType)
        if exist:
            break
        else:
            print("Invalid option")
    if newType == 1:
        newType = "Cautious"
    elif newType == 2:
        newType = "Moderated"
    elif newType == 3:
        newType = "Bold"
    print("\nName:".ljust(10) + newName + "\nDNI:".ljust(10) + newNif + "\nProfile:".ljust(10) + newType)
    if newType == "Cautious":
        newType = 30
    elif newType == "Moderated":
        newType = 40
    elif newType == "Bold":
        newType = 50
    confirm = input("Are this values right? Y/y = yes | N/n = no: ")
    if confirm.lower() == "y" or confirm.lower() == "yes":
        con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306)
        newHum = (newNif, newName, newType, True)
        try:
            with con.cursor() as cur:
                cur.execute('INSERT INTO player VALUES (%s, %s, %s, %s)', (newHum[0], newHum[1], newHum[2], newHum[3]))
                con.commit()
        finally:
            con.close()
    print("\n")


def newBoot():
    width = os.get_terminal_size().columns
    print("*" * width + "\n")
    print(pyfiglet.figlet_format("New Bot Player"))
    print("\n" + "*" * width + "\n")
    while True:
        newName = input("Name: ")
        if newName.isalnum() is False:
            print("\nIncorrect name. The name introduced must only contain letters and numbers and not have spaces.\n")
        else:
            break
    while True:
        nifletter = "TRWAGMYFPDXBNJZSQVHLCKE"
        nifNum = []
        for i in range(0, 8):
            nifNum.append(str(random.randint(0,9)))
        newNif = ""
        for num in nifNum:
            newNif += num
        newNif += nifletter[int(newNif)%23]
        playersID = allPlayersID()
        exist = False
        for existingNif in playersID:
            if existingNif[0] == newNif:
                exist = True
        if not exist:
            break
    print("\nName:".ljust(10) + newName + "\nDNI:".ljust(10) + newNif)
    while True:
        newType = input("\nSelect profile for the new boot: \n1)Cautious \n2)Moderated \n3)Bold \nOption: ")
        options = [1, 2, 3]
        exist = False
        for value in options: 
            if str(value) == newType:
                exist = True
                newType = int(newType)
        if exist:
            break
        else:
            print("Invalid option")
    if newType == 1:
        newType = "Cautious"
    elif newType == 2:
        newType = "Moderated"
    elif newType == 3:
        newType = "Bold"
    print("\nName:".ljust(10) + newName + "\nDNI:".ljust(10) + newNif + "\nProfile:".ljust(10) + newType)
    if newType == "Cautious":
        newType = 30
    elif newType == "Moderated":
        newType = 40
    elif newType == "Bold":
        newType = 50
    confirm = input("Are this values right? Y/y = yes | N/n = no: ")
    if confirm.lower() == "y" or confirm.lower() == "yes":
        con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306)
        newBot = (newNif, newName, newType, False)
        try:
            with con.cursor() as cur:
                cur.execute('INSERT INTO player VALUES (%s, %s, %s, %s)', (newBot[0], newBot[1], newBot[2], newBot[3]))
                con.commit()
        finally:
            con.close()
    print("\n")
        

def printAllPlayers(banner):
    width = os.get_terminal_size().columns
    print("*" * width + "\n")
    print(pyfiglet.figlet_format(banner))
    print("\n" + "*" * width + "\n")
    con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
    players = {}
    try:
        with con.cursor() as cur:
            cur.execute("SELECT * from player")
            rows = cur.fetchall()
            for player in rows:
                players[player["player_id"]] = {}
                players[player["player_id"]]["name"] = player["player_name"]
                players[player["player_id"]]["type"] = player["player_risk"]
                players[player["player_id"]]["human"] = bool(player["human"])
    finally:
        con.close()
    for player in players:
        if players[player]["type"] == 30:
            players[player]["type"] = "Cautious"
        elif players[player]["type"] == 40:
            players[player]["type"] = "Moderated"
        elif players[player]["type"] == 50:
            players[player]["type"] = "Bold"
    print("*"*60 + "\nBoot Players" + "\n" + "-"*60 + "\nID".ljust(20) + "Name".ljust(20) + "Type".ljust(20) + "\n" + "-"*60) 
    for player in players:
        if players[player]["human"] is False:
            print(player.ljust(19) + players[player]["name"].ljust(20) + players[player]["type"].ljust(20))
    print("*"*60 + "\nHuman Players" + "\n" + "-"*60 + "\nID".ljust(20) + "Name".ljust(20) + "Type".ljust(20) + "\n" + "-"*60)
    for player in players:
        if players[player]["human"] is True:
            print(player.ljust(19) + players[player]["name"].ljust(20) + players[player]["type"].ljust(20))
    print("*"*60 + "\n")


def removePlayer():
    while True:
        printAllPlayers("Show-Remove Players")
        sel = input("Option (-id to remove player, -1 to exit): ")
        con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
        players = {}
        try:
            with con.cursor() as cur:
                cur.execute("SELECT * from player")
                rows = cur.fetchall()
                for player in rows:
                    players[player["player_id"]] = {}
        finally:
            con.close()
        if sel == "-1":
            print("\n")
            break
        elif sel[0] == "-" and len(sel) == 10:
            exist = False
            for player in players:
                if player == sel[1:]:
                    exist = True
            if exist:
                con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
                players = {}
                try:
                    with con.cursor() as cur:
                        cur.execute("DELETE FROM player WHERE player_id = %s", (sel[1:]))
                        cur.execute("DELETE FROM player_game_round WHERE player_id = %s", (sel[1:]))
                        cur.execute("DELETE FROM player_game WHERE player_id = %s", (sel[1:]))
                        con.commit()
                        print("\nPlayer deleted")
                        input("\nEnter to continue\n") 
                finally:
                    con.close()
            else:
                print("\nInvalid Option")
                input("\nEnter to continue\n") 
        else:
            print("\nInvalid Option")
            input("\nEnter to continue\n")


def setGamePlayer():
    while True:
        printAllPlayers("Set Game Players")
        sel = input("Option (-id to remove player, -1 to exit): ")
        con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
        players = {}
        try:
            with con.cursor() as cur:
                cur.execute("SELECT * from player")
                rows = cur.fetchall()
                for player in rows:
                    players[player["player_id"]] = {}
        finally:
            con.close()
        if sel == "-1":
            print("\n")
            break
        elif sel == "" or len(sel) < 9:
            print("\nInvalid Option")
            input("\nEnter to continue\n") 
        elif sel[0] != "-" and len(sel) == 9:
            exist = False
            for player in players:
                if player == sel:
                    exist = True
            repeat = False
            for player in data.game:
                if player == sel:
                    repeat = True
            if exist and repeat is False:
                con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
                allPlayers = {}
                try:
                    with con.cursor() as cur:
                        cur.execute("SELECT * FROM player")
                        rows = cur.fetchall()
                        for player in rows:
                            allPlayers[player["player_id"]] = {}
                            allPlayers[player["player_id"]]["name"] = player["player_name"]
                            allPlayers[player["player_id"]]["type"] = player["player_risk"]
                            allPlayers[player["player_id"]]["human"] = player["human"]
                        data.players[sel] = {}
                        data.players[sel]["name"] = allPlayers[sel]["name"]
                        data.players[sel]["human"] = bool(allPlayers[sel]["human"])
                        data.players[sel]["bank"] = False
                        data.players[sel]["initialCard"] = ""
                        data.players[sel]["priority"] = 0
                        data.players[sel]["type"] = allPlayers[sel]["type"]
                        data.players[sel]["bet"] = 0
                        data.players[sel]["points"] = 0
                        data.players[sel]["cards"] = []
                        data.players[sel]["roundPoints"] = 0
                        data.game.append(sel) 
                        print("\n" + "*"*20 + "Actual Players in Game" + "*"*20)
                        for player in data.game:
                            if data.players[player]["human"] is True:
                                print(player.ljust(15) + data.players[player]["name"].ljust(15) + "True".ljust(15) + str(data.players[player]["type"]).ljust(15))
                            elif data.players[player]["human"] is False:
                                print(player.ljust(15) + data.players[player]["name"].ljust(15) + "False".ljust(15) + str(data.players[player]["type"]).ljust(15))
                        input("\nEnter to continue\n")
                finally:
                    con.close()
            else:
                print("\nInvalid Option")
                input("\nEnter to continue\n") 
        elif sel[0] == "-" and len(sel) == 10:
            exist = False
            for player in data.game:
                if player == sel[1:]:
                    exist = True
            if exist:
                data.players.pop(sel[1:])
                data.game.remove(sel[1:])
                print("\n" + "*"*20 + "Actual Players in Game" + "*"*20)
                for player in data.game:
                    if data.players[player]["human"] is True:
                        print(player.ljust(15) + data.players[player]["name"].ljust(15) + "True".ljust(15) + str(data.players[player]["type"]).ljust(15))
                    elif data.players[player]["human"] is False:
                        print(player.ljust(15) + data.players[player]["name"].ljust(15) + "False".ljust(15) + str(data.players[player]["type"]).ljust(15))
                input("\nEnter to continue\n")
            else:
                print("\nInvalid Option")
                input("\nEnter to continue\n")
        else:
            print("\nInvalid Option")
            input("\nEnter to continue\n")
        

def sendCardgame(cardgame):
    con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
    try:
        with con.cursor() as cur:
            cur.execute('INSERT INTO cardgame VALUES (%s, %s, %s, %s, %s, %s)', (cardgame["cardgame_id"], cardgame["players"], cardgame["rounds"], cardgame["start_hour"], cardgame["end_hour"], cardgame["deck_id"]))
            con.commit()
    finally:
        con.close()


def sendPlayer_game(player_game):
    gameid = list(player_game.keys())[0]
    for player in player_game[gameid]:
        playerStats = player_game[gameid][player]
        con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
        try:
            with con.cursor() as cur:
                cur.execute('INSERT INTO player_game VALUES (%s, %s, %s, %s, %s)', (gameid, player, playerStats["initial_card_id"], playerStats["starting_points"], playerStats["ending_points"]))
                con.commit()
        finally:
            con.close()


def sendPlayer_round_game(player_round_game):
    gameid = list(player_round_game.keys())[0]
    for round in player_round_game[gameid]:
        for player in player_round_game[gameid][round]:
            playerStats = player_round_game[gameid][round][player]
            con = pymysql.connect(host='proyecto-global-gjm.mysql.database.azure.com', user='administrador', password='Pr0jectoGJM', database='7ymedio', port=3306, cursorclass=pymysql.cursors.DictCursor)
            try:
                with con.cursor() as cur:
                    cur.execute('INSERT INTO player_game_round VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (gameid, round, player, playerStats["is_bank"], playerStats["bet_points"], playerStats["cards_value"], playerStats["starting_round_points"], playerStats["ending_round_points"]))
                    con.commit()
            finally:
                con.close()




