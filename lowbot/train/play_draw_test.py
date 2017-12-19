import random
from lowbot.poker.game import *
from lowbot.poker.hands import *
from lowbot.poker.deck import *

my_score = 0.
game_num = 0

def getAction(p):
    r = random.random()
    if r < p:
        return "p"
    else:
        return "b"

def playGame():
    game = Game()
    print("BB cards are {0}".format(game.Hands[0].to_string()))
    print("AI card was {0}".format(game.Hands[1].to_string()))
    score = cfr(game)
    print("Winner is {0}".format(game.Winner))
    print("Score is {0}".format(score))
    print("")
    return score



def cfr(game):

    actions = game.get_legal_actions()


    return cfr(game)

playGame()
