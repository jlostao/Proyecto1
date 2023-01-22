import functions
import data
import time

m00 = True
m01 = False
m02 = False
m03 = False
m04 = False
m05 = False

rounds = 5
seldeck = 0

while True:
    while m00:
        sel = functions.menuFunct("Siete y medio", "1) Add/Remove/Show Players \n2) Settings \n3) Play Game \n4) Ranking \n5) Reports \n6) Exit", "Option: ", [1, 2, 3, 4, 5, 6])
        print("\n")
        if sel == 1:
            m01 = True
            m00 = False
        elif sel == 2:
            m02 = True
            m00 = False
        elif sel == 3:
            if len(data.game) < 2 or len(data.game) > 6:
                print("Set the players that compose the game first.")
                input("\nEnter to continue\n")
            else:
                if seldeck == 0:
                    print("Select a deck of cards first")
                    input("\nEnter to continue\n")
                else:
                    m03 = True
                    m00 = False
        elif sel == 4:
            m04 = True
            m00 = False
        elif sel == 5:
            m05 = True
            m00 = False
        elif sel == 6:
            exit()

    while m01:
        sel = functions.menuFunct("BBDD Players", "1) New Human Player \n2) New Boot \n3) Show/Remove Players \n4) Go back", "Option: ", [1, 2, 3, 4])
        if sel == 1:
            functions.newHuman()
        elif sel == 2:
            functions.newBoot()
        elif sel == 3:
            print("Show/Remove Players")
        elif sel == 4:
            m00 = True
            m01 = False

    while m02:
        sel = functions.menuFunct("Settings", "1) Set Game Players \n2) Set Card's Deck \n3) Set Max Rounds (Default 5 Rounds) \n4) Go back", "Option: ", [1, 2, 3, 4])
        if sel == 1:
            print("Set players")
        elif sel == 2:
            seldeck = functions.menuFunct("Deck Of Cards", "1) ESP - ESP \n2) POK - POK \n0) Go back", "Option: ", [1, 2, 0])
            functions.setGameCards(seldeck)
            if seldeck == 1:
                print("\nEstablished Card Deck ESP, Baraja Española")
            elif seldeck == 2:
                print("\nEstablished Card Deck POK, Poker Deck")
            elif seldeck == 0:
                print("\nNo deck selected")
            input("\nEnter to continue\n")
        elif sel == 3:
            while True:
                rounds = input("Max Rounds: ")
                if rounds.isdigit() is False:
                    print("Please, only enter numbers")
                    input("\nPress enter to continue\n")
                elif rounds.isdigit():
                    rounds = int(rounds)
                    if rounds <= 0:
                        print("Please, enter only positive numbers")
                        input("\nPress enter to continue\n")
                    elif rounds > 0:
                        print("Established max rounds to " + str(rounds))
                        input("\nPress enter to continue\n")
                        break
        elif sel == 4:
            m00 = True
            m02 = False

    while m03:
        functions.playGame(rounds, seldeck)
        m00 = True
        m03 = False


    while m04:
        sel = functions.menuFunct("Ranking", "1) Players With More Earnings \n2) Players With More Games Played \n3) Players With More Minutes Played \n4) Go back", "Option: ", [1, 2, 3, 4])
        if sel == 1:
            print("More earnings")
        elif sel == 2:
            print("More games")
        elif sel == 3:
            print("More minutes")
        elif sel == 4:
            m04 = False
            m00 = True

    while m05:
        sel = functions.menuFunct("Reports", "1) Initial card more repeated by each user, only users who have played a minimum of 3 games. \n2) Player who makes the highest bet per game, find the round with the highest bet. \n3) Player who makes the lowest bet per game. \n4) Percentage of rounds won per player in each game (%), as well as their average bet for the game. \n5) List of games won by Bots. \n6) Rounds won by the bank in each game. \n7) Number of users that have been the bank in each game. \n8)Average bet per game. \n9) Average bet of the first round of each game. \n10) Average bet of the last round of each game. \n11) Go back", "Option: ", [1, 2, 3, 4])
        if sel == 1:
            print("Initial card repeated")
        elif sel == 2:
            print("Highest bet per game")
        elif sel == 3:
            print("Lowest bet per game")
        elif sel == 4:
            print("Percentage rounds won per player")
        elif sel == 5:
            print("Games won by bots")
        elif sel == 6:
            print("Rounds won by bank")
        elif sel == 7:
            print("Users tha have been bank per game")
        elif sel == 8:
            print("Average bet per game")
        elif sel == 9:
            print("Average bet first round of game")
        elif sel == 10:
            print("Average bet last round of game")
        elif sel == 11:
            m00 = True
            m05 = False