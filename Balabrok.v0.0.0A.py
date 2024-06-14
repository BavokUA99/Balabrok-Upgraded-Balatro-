import random
import os
import time

cardsUsed = 0
allHand = []
playHand = []
playHandId = []

BATTLE = False

HANDS = [5, 5]
DISCARDS = [5, 5]
MONEY = 4
HANDSIZE = 11
HANDPLAY = 6
ANTE = 1
ROUND = 1

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades", "Moons", "Stars", "Moles", "Arenels"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "J", "P", "Q", "K", "A"]

DECK = [[j, i, "N", "N", "N"] for j in RANKS for i in SUITS] #[Rank, Suit, Enchantment, Edition, Seal]

HANDINFO = {"High Card" : [1, 5, 1, 10, 1, "Mercury"], "Duo" : [1, 10, 2, 15, 1, "Venus"], "Dobble Duo" : [1, 20, 2, 15, 2, "Mars"], 
            "Trio" : [1, 30, 3, 15, 2, "Earth"], "Semi-Full House" : [1, 35, 4, 25, 3, "Phobos"], "Duo Full House" : [1, 40, 4, 25, 3, "Deimos"], 
            "Quartetto" : [1, 45, 5, 30, 3, "Ceres"], "Straight" : [1, 55, 5, 50, 4, "The Moon"], "Full House" : [1, 60, 5, 35, 3, "Uranus"], 
            "Trio Full House" : [1, 60, 6, 35, 3, "Neptune"], "Quintetto" : [1, 70, 7, 40, 4, "Pluto"], "Sextetto" : [1, 100, 10, 50, 5, "Eris"],
            
            "Spectrum" : [1, 25, 2, 20, 2, "Jupiter"], "Straight Spectrum" : [1, 65, 6, 60, 5, "Metis"], "Spectrum (Semi-) House" : [1, 45, 4, 40, 4, "Amalthea"], 
            "Spectrum (Duo) House" : [1, 50, 4, 40, 4, "Thebe"], "Spectrum House" : [1, 70, 5, 45, 4, "Io"], "Spectrum (Trio) House" : [1, 70, 6, 45, 4, "Europa"], 
            "Spectrum Quintetto" : [1, 75, 7, 45, 5, "Ganymede"], "Spectrum Sextetto" : [1, 105, 10, 55, 5, "Callisto"],

            "Flush" : [1, 85, 8, 45, 5, "Saturn"], "Straight Flush" : [1, 130, 14, 90, 8, "Mimas"], "Flush (Semi-) House" : [1, 140, 15, 100, 9, "Enceladus"], 
            "Flush (Duo) House" : [1, 145, 16, 100, 9, "Tethys"], "Flush House" : [1, 155, 17, 110, 9, "Dione"], "Flush (Trio) House" : [1, 160, 18, 110, 9, "Rhea"], 
            "Flush Quintetto" : [1, 180, 20, 120, 10, "Titan"], "Flush Sextetto" : [1, 200, 25, 150, 12, "Iapetus"]
            } #Hand : [Lvl, Chips, Mult, ChipsXLvl, MultXLvl, Planet Card]

ANTES = {0 : "100", 1 : "500", 2 : "2000", 3 : "8000", 4 : "30000", 5 : "110000", 6 : "400000", 7 : "1400000", 8 : "4500000", 9 : "13500000", 10 : "40000000"}
ROUNDS = [1, 1.5, 2, 3]

def Fibonacci(num):
    a = 1
    b = 1
    for i in range(num - 2):
        if i % 2 != 0:
            a = b + a
        else:
            b = a + b
    
    res = 0
    
    if num % 2 != 0:
        res = b
    else:
        res = a
    
    return res

def round(num):
    global HANDS
    global DISCARDS
    global cardsUsed
    global allHand
    global playHand
    global playHandId
    global BATTLE

    chipsToWin = ROUNDS[num] * float(ANTES[ANTE])
    cardsUsed = 0
    totChips = 0
    allHand = []
    playHand = []
    playHandId = []
    BATTLE = True
    HANDS[1] = HANDS[0]
    DISCARDS[1] = DISCARDS[0]

    for i in range(HANDSIZE):
        allHand.append(DECK[cardsUsed])
        cardsUsed += 1
        
    while(BATTLE):
        report(chipsToWin, totChips)

        allStr = []
        playStr = []

        for i in allHand:
            allStr.append(i[0:2])
        print(allStr, "\n\n")
        for i in playHand:
            playStr.append(i[0:2])
        print(playStr)

        action = input()

        if action == "PLAY":
            Chips = 0
            Mult = 0
            posibleHands = handIdentity(playHand)
            print(posibleHands)
            HANDS[1] -= 1

            handId = int(input())
            Chips += HANDINFO[posibleHands[handId - 1]][1]
            Mult += HANDINFO[posibleHands[handId - 1]][2]

            for i in playHand:
                if i[0] == "J":
                    Chips += 12
                    Mult += 0.25
                elif i[0] == "P":
                    Chips += 12
                    Mult += 0.5
                elif i[0] == "Q":
                    Chips += 12
                    Mult += 0.75
                elif i[0] == "K":
                    Chips += 12
                    Mult += 1
                elif i[0] == "A":
                    Chips += 13
                    Mult += 1
                else:
                    Chips += int(i[0])
            
            totChips += Chips * Mult

            if totChips >= chipsToWin:
                report(chipsToWin, totChips)
                print("You've beaten it! Ready to go deeper?")
                time.sleep(5)
                print("Welp, I don't care if you're ready or not, here we go!")
                time.sleep(3)
                BATTLE = False
            elif HANDS[1] == 0:
                print("GAME OVER!!!")
                exit(0)

            drawCards()

        elif action == "DISC":
            if DISCARDS[1] != 0:
                DISCARDS[1] -= 1
                drawCards()
            else:
                print("You have no discards left!")
                time.sleep(1)
        else:
            try: 
                Id = int(action)
                cardSel = False
                for i in playHandId:
                    if i == Id - 1:
                        cardSel = True
                        playHand.remove(allHand[i])
                        playHandId.remove(i)

                if len(playHand) < HANDPLAY and cardSel == False and Id > 0:
                    playHand.append(allHand[Id - 1])
                    playHandId.append(Id - 1)
                elif cardSel == True:
                    pass
                elif Id <= 0:
                    print("You haven't got", Id, "cards!")
                    time.sleep(1)
                else:
                    print("You're not allowed to play more than", HANDPLAY, "cards!")
                    time.sleep(1)

            except IndexError:
                print("You haven't got", Id, "cards!")
                time.sleep(1)
            except ValueError:
                print("This action isn't in the game!")
                time.sleep(1)

def drawCards():
    global cardsUsed
    global allHand
    global playHand
    global playHandId

    for i in range(len(playHandId) - 1): #Orginizes the ranks of the hand by order
        for j in range(len(playHandId) - i - 1):
            if playHandId[j] < playHandId[j + 1]:
                playHandId[j], playHandId[j + 1] = playHandId[j + 1], playHandId[j]
    
    for i in playHandId:
        allHand.remove(allHand[i])
        allHand.append(DECK[cardsUsed])
        cardsUsed += 1
        playHand = []
        playHandId = []

def report(chipsToWin, totChips):
    global HANDS
    global DISCARDS

    os.system("cls")
    print("Chips to win: ", chipsToWin, "\n", "Current Chips: ", totChips, "\n", "Hands: ", HANDS[1], "   Discards: ", DISCARDS[1], "\n\n\n")

def handIdentity(hand):
    suitQuant = {"Hearts" : 0, "Diamonds" : 0, "Clubs" : 0, "Spades" : 0, "Moons" : 0, "Stars" : 0, "Moles" : 0, "Arenels" : 0}
    handSuitType = ["Default"]
    suits = 0

    for i in range(len(hand)): #Orginizes the hands in suits, by how many cards there are of determined suits
        suitQuant[hand[i][1]] += 1

    for i in suitQuant.values(): #Defines how many suits is there in this hand
        if i != 0:
            suits += 1

    if suits == 1 and len(hand) == 6: #Defines the type of the hand based on the suit
        handSuitType.append("Flush") 
    elif suits == 6:
        handSuitType.append("Spectrum")

    rankQuant = {"1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "10" : 0, "11" : 0, "12" : 0, "J" : 0, "P" : 0, "Q" : 0, "K" : 0, "A" : 0}
    handNumType = ["High Card"]
    quants = []
    quantsQuant = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}
    nums = []

    for i in range(len(hand)): #Orginizes the hands in ranks, by how many cards there are of determined ranks
        rankQuant[hand[i][0]] += 1

    for i in rankQuant.values(): #Gives a list of number of ranks in this hand
        if i != 0:
            quants.append(i)

    for i in quants: #Says how many singles, duos, trios, etc there are in the hand
        quantsQuant[i] += 1

    if quantsQuant[2] >= 1 or quantsQuant[3] >= 1 or quantsQuant[4] == 1 or quantsQuant[5] == 1 or quantsQuant[6] == 1: #Qualifies the hand type (by pairs, trios ...)
        handNumType.append("Duo")
    if quantsQuant[2] >= 2 or (quantsQuant[2] == 1 and (quantsQuant[3] == 1 or quantsQuant[4] == 1)) or quantsQuant[3] == 2:
        handNumType.append("Dobble Duo")
    if quantsQuant[2] == 3:
        handNumType.append("Duo Full House")
    if quantsQuant[3] >= 1 or quantsQuant[4] == 1 or quantsQuant[5] == 1 or quantsQuant[6] == 1:
        handNumType.append("Trio")
    if quantsQuant[3] == 2:
        handNumType.append("Trio Full House")
    if (quantsQuant[2] == 1 and (quantsQuant[3] == 1 or quantsQuant[4] == 1)) or quantsQuant[3] == 2:
        handNumType.append("Semi-Full House")  
    if quantsQuant[2] == 1 and quantsQuant[4] == 1:
        handNumType.append("Full House")
    if quantsQuant[4] == 1 or quantsQuant[5] == 1 or quantsQuant[6] == 1:
        handNumType.append("Quartetto")
    if quantsQuant[5] == 1 or quantsQuant[6] == 1:
        handNumType.append("Quintetto")
    if quantsQuant[6] == 1:
        handNumType.append("Sextetto")

    for i in range(len(hand)): #Gives list of ranks of the cards 
        if hand[i][0] == "J":
            nums.append(13)
        elif hand[i][0] == "P":
            nums.append(14)
        elif hand[i][0] == "Q":
            nums.append(15)
        elif hand[i][0] == "K":
            nums.append(16)
        elif hand[i][0] == "A":
            nums.append(17)
        else:
            nums.append(int(hand[i][0]))

    if len(hand) == HANDPLAY:
        for i in range(5): #Orginizes the ranks of the hand by order
            for j in range(5 - i):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]

        for i in range(HANDPLAY): #Checks-in if this hand is a straight
            if i == HANDPLAY - 1:
                handNumType.append("Straight")
                break

            if nums[i] + 1 != nums[i + 1]:
                break

    handSort = []

    for i in handSuitType: #Gets all poker hands you can play
        for j in handNumType:
            if i == "Default":
                handSort.append(j)

            elif i == "Flush":
                if j == "Duo Full House":
                    handSort.append("Flush (Duo) House")
                elif j == "Trio Full House":
                    handSort.append("Flush (Trio) House")
                elif j == "Semi-Full House":
                    handSort.append("Flush (Semi-) House")
                elif j == "Full House":
                    handSort.append("Flush House")
                elif j == "Quintetto":
                    handSort.append("Flush Quintetto")
                elif j == "Sextetto":
                    handSort.append("Flush Sextetto")
                elif j == "Straight":
                    handSort.append("Straight Flush")
                else:
                    isFlushSort = False
                    for k in handSort:
                        if k == "Flush":
                            isFlushSort = True
                    
                    if isFlushSort == False:
                        handSort.append("Flush")

            elif i == "Spectrum":
                if j == "Duo Full House":
                    handSort.append("Spectrum (Duo) House")
                elif j == "Trio Full House":
                    handSort.append("Spectrum (Trio) House")
                elif j == "Semi-Full House":
                    handSort.append("Spectrum (Semi-) House")
                elif j == "Full House":
                    handSort.append("Spectrum House")
                elif j == "Quintetto":
                    handSort.append("Spectrum Quintetto")
                elif j == "Sextetto":
                    handSort.append("Spectrum Sextetto")
                elif j == "Straight":
                    handSort.append("Straight Spectrum")
                else:
                    isSpectrumSort = False
                    for k in handSort:
                        if k == "Spectrum":
                            isSpectrumSort = True
                    
                    if isSpectrumSort == False:
                        handSort.append("Spectrum")
    return handSort

def main():
    global DECK
    while(True):
        for i in range(4):
            random.shuffle(DECK)
            round(i)
        break

if __name__ == "__main__":
    main()