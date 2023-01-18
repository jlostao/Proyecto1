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
                data.players[player]["bet"] = (data.players[player]["points"] * data.players[player]["type"]) / 100


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


def playGame(round, deck):
    setGamePriority()
    resetPoints()
    #while round > 0 and check2PlayersWithPoints():
    setGameCards(deck)
    setBets()
    for player in data.game:
        if data.players[player]["bank"] is False:
            standarRound(player)
    for player in data.game:
        if data.players[player]["bank"] is True:
            bootBankRound(player)
    for player in data.game:
        print(player, data.players[player]["priority"], data.players[player]["bank"], data.players[player]["points"], data.players[player]["bet"], data.players[player]["cards"], data.players[player]["roundPoints"])
    
    

 