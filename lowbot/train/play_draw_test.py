import random
from lowbot.poker.game import *
from lowbot.poker.hands import *
from lowbot.poker.deck import *

my_score = 0.
game_num = 0


def get_action(p):
    r = random.random()
    if r < p:
        return "p"
    else:
        return "b"


def play_game():
    game = Game(num_draws=1)
    print("SB cards are {0}".format(game.Hands[0].to_string()))
    print("BB card was {0}".format(game.Hands[1].to_string()))
    score = cfr(game)
    print("SB cards are {0}".format(game.Hands[0].to_string()))
    print("BB card was {0}".format(game.Hands[1].to_string()))
    print("Winner is {0}".format(game.Winner))
    print("Score is {0}".format(score))
    print("")
    return score


def cfr(game):

    if game.State == TERMINAL:
        if game.get_winner() == 2:
            return 0
        else:
            return game.Pots[1 - game.get_winner()]

    actions = game.get_legal_actions()
    action = input("Player{0}, pick action from: {1} ".format(game.get_current_player(), actions))
    indices = ""
    if action == "d":
        indices = [int(x) for x in input("Pick cards (0-4): ").split()]
    game.perform_action(action, indices)

    return cfr(game)


play_game()
