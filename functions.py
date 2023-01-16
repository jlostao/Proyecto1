import data
import pyfiglet
import os
import random


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
    gamecards = []
    for card in data.cards:
        if deck == 1:
            if card[0] == "O" or card[0] == "E" or card[0] == "C" or card[0] == "B":
                gamecards.append(card)
                
        elif deck == 2:
            if card[0] == "H" or card[0] == "D" or card[0] == "T" or card[0] == "P":
                gamecards.append(card)
    if deck == 1:
        print("\nEstablished Card Deck ESP, Baraja Española")
    elif deck == 2:
        print("\nEstablished Card Deck POK, Poker Deck")
    elif deck == 0:
        print("\nNo deck selected")
    return gamecards
    

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
        if data.players[player]["points"] < 0:
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
    bets = []
    for player in data.game:
        if data.players[player]["type"] == 40:
            if data.players[player]["points"] <= 5:
                min = data.players[player]["points"]
            else:
                min = 5
            if data.players[player]["points"] <= 5:
                max = data.players[player]["points"]
            else:
                if (40*data.players[player]["points"])//100 <= 5:
                    max = 5
                else:
                    max = (40*data.players[player]["points"])//100
            bets.append(random.randint(min, max))
        elif data.players[player]["type"] == 50:
            if data.players[player]["points"] <= 5:
                min = data.players[player]["points"]
            else:
                if (30*data.players[player]["points"])//100 <= 5:
                    min = 5
                else:
                    min = (30*data.players[player]["points"])//100
            if data.players[player]["points"] <= 5:
                max = data.players[player]["points"]
            else:
                if (60*data.players[player]["points"])//100 <= 5:
                    max = 5
                else:
                    max = (60*data.players[player]["points"])//100
            bets.append(random.randint(min, max))
        elif data.players[player]["type"] == 60:
            if data.players[player]["points"] <= 5:
                min = data.players[player]["points"]
            else:
                if (50*data.players[player]["points"])//100 <= 5:
                    min = 5
                else:
                    min = (50*data.players[player]["points"])//100
            if data.players[player]["points"] <= 5:
                max = data.players[player]["points"]
            else:
                if (80*data.players[player]["points"])//100 <= 5:
                    max = 5
                else:
                    max = (80*data.players[player]["points"])//100
            bets.append(random.randint(min, max))
    for i in range(len(data.game)):
        data.players[data.game[i]]["bet"] = bets[i]


def playGame():
    setGamePriority()
    resetPoints()
    setBets()
    print(data.game)
    print(data.players)
    

 