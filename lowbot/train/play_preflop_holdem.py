import random
from lowbot.poker.hands import Hand
from lowbot.poker.deck import *

my_score = 0.
game_num = 0

f = None
with open('strategy.csv') as a:
    f = a.read()

strategy = {}
for row in f.splitlines():
    a = row.split(',')

    strategy[a[0]] = float(a[1])

deck = Deck()

def getAction(p):
    r = random.random()
    if r < p:
        return "p"
    else:
        return "b"

def playGame(ai_strategy, cards, hero_position, score):
    cards.shuffle()
    history = ""
    hands = [Hand(cards.Cards[0:2]), Hand(cards.Cards[2:4])]
    playerHand = hands[hero_position]
    oppHand = hands[1-hero_position]

    print("Your card is {0}".format(playerHand.to_string()))
    score += cfr(cards, history, ai_strategy, hero_position, playerHand, oppHand)
    print("AI card was {0}".format(oppHand.to_string()))
    print("Your score = {0}".format(score))
    print("")
    return score



def cfr(cards, history, ai_strategy, position, playerHand, oppHand):
    plays = len(history)
    player = plays % 2
    opponent = 1 - player

    if plays > 1:
        terminalPass = history[plays - 1] == 'p'
        doubleBet = history.endswith("bb")
        isPlayerCardHigher = playerHand.compare(oppHand)

        if terminalPass:
            if history == "pp":
                return isPlayerCardHigher
            else:
                return 1 if player == position else -1
        elif doubleBet:
            return 2 * isPlayerCardHigher

    infoSet = str(oppHand.to_string_simplified()) + history

    action = ""

    if player == position:
        action = input("Select an action [p/b]: ")
        print("Player plays {0}".format(action))
    else:
        action = getAction(ai_strategy[infoSet])
        print("AI plays {0}".format(action))

    history += action

    return cfr(cards, history, ai_strategy, position, playerHand, oppHand)

while game_num < 100000:
    game_num += 1
    print("Game nuber: {0}".format(game_num))
    my_score = playGame(strategy, deck, 0, my_score)
    game_num += 1
    print("Game nuber: {0}".format(game_num))
    my_score = playGame(strategy, deck, 1, my_score)
