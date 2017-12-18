import numpy as np
import random

my_score = 0.
game_num = 0

f = None
with open('13cards.csv') as a:
    f = a.read()

strategy = {}
for row in f.splitlines():
    a = row.split(',')

    strategy[a[0]] = float(a[1])/100

deck = [i for i in range(13)]

def getAction(p):
    r = random.random()
    if r < p:
        return "p"
    else:
        return "b"

def playGame(ai_strategy, cards, hero_position, score):
    cards = np.random.permutation(cards)
    history = ""

    print("Your card is {0}".format(cards[hero_position]))
    score += cfr(cards, history, ai_strategy, hero_position)
    print("AI card was {0}".format(cards[1-hero_position]))
    print("Your score = {0}".format(score))
    print("")
    return score



def cfr(cards, history, ai_strategy, position):
    plays = len(history)
    player = plays % 2

    if plays > 1:
        terminalPass = history[plays - 1] == 'p'
        doubleBet = history.endswith("bb")
        isPlayerCardHigher = cards[position] > cards[1 - position]

        if terminalPass:
            if history == "pp":
                return 1 if isPlayerCardHigher else -1
            else:
                return 1 if player == position else -1
        elif doubleBet:
            return 2 if isPlayerCardHigher else -2

    infoSet = str(cards[player]) + history

    action = ""

    if player == position:
        action = input("Select an action [p/b]: ")
    else:
        action = getAction(ai_strategy[infoSet])
        print("AI plays {0}".format(action))

    history += action

    return cfr(cards, history, ai_strategy, position)

while True:
    game_num += 1
    print("Game nuber: {0}".format(game_num))
    my_score = playGame(strategy, deck, 0, my_score)
    game_num += 1
    print("Game nuber: {0}".format(game_num))
    my_score = playGame(strategy, deck, 1, my_score)
