import data
import pyfiglet
import os
import random
import time


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



def humanRound(id):
    print("human")


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
            print(aboveCard/len(data.deck) * 100)
            break
    

def humanBankRound(id):
    print("human")


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
        if data.players[player]["bank"] is True and bankCandidate == [] and data.players[player]["points"] <= 0:
            data.players[player]["bank"] = False
            data.game.remove(player)
            data.players[data.game[0]]["bank"] = True
    if bankCandidate != []:
        for player in data.game:
            if data.players[player]["bank"] is True:
                data.players[player]["bank"] = False
        newBank = bankCandidate[random.randint(0, len(bankCandidate) - 1)]
        data.players[newBank]["bank"] = True
    

def printStats(id, round):
    if id == "a":
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
        print("*"*50 + "\n")
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
        print("*"*20 + " Round " + str(round) + ", Turn of " + data.players[id]["name"] + " " + "*"*20 + "\n")
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
    print(data.game)
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
    

def playGame(round, deck):
    setGamePriority()
    resetPoints()
    currentround = 1
    while round > 0 and check2PlayersWithPoints():
        data.roundPrint = {"name":"Name".ljust(20), "human":"Human".ljust(20), "priority":"Priority".ljust(20), "type":"Type".ljust(20), "bank":"Bank".ljust(20), 
                           "bet":"Bet".ljust(20), "points":"Points".ljust(20), "cards":"Cards".ljust(20), "roundpoints":"Roundpoints".ljust(20)}
        setGameCards(deck)
        setBets()
        printStats("a", currentround)
        for i in range(len(data.game) - 1, -1, -1):
            if data.players[data.game[i]]["bank"] is False:
                standarRound(data.game[i])
                printStats(data.game[i], currentround)
        for player in data.game:
            if data.players[player]["bank"] is True:
                bootBankRound(player)
                printStats(player, currentround)
        distributionPointAndNewBankCandidates()
        printStats("b", round)
        orderPlayersByPriority()
        resetStats()
        currentround += 1
        round -= 1
    

 