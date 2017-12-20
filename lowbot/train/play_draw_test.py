import random
from lowbot.poker.game import *
from lowbot.poker.hands import *
from lowbot.poker.deck import *

my_score = 0.
game_num = 0


f = None
with open('strategy.csv') as a:
    f = a.read()

strategy = {}
for row in f.splitlines():
    a = row.split(',')

    strategy[a[0]] = list(map(float, a[2:]))


def get_action(actions, strat):
    r = random.random()
    a = 0
    cumulativeProbability = 0
    while a < len(strat) - 1:
        cumulativeProbability += strat[a]
        if r < cumulativeProbability:
            break
        a += 1

    indices = []
    if actions == "d":
        for i, c in enumerate(format(a, '01b')):
            if c == "1":
                indices.append(i)
        action = "d"
    else:
        action = actions[a]

    return [action, indices]


def play_game(position):
    game = Game(num_draws=1, hand_size=1, num_cards=13, cap=2)
    if position == 0:
        print("You're on the SB")
    else:
        print("Your're on the BB")
    print("Your cards are {0}".format(game.Hands[position].to_string()))
    score = cfr(game, position)
    print("Your cards are {0}".format(game.Hands[position].to_string()))
    print("Opponent card are {0}".format(game.Hands[1-position].to_string()))
    print("Your score is {0}".format(score if position == game.get_winner() else -score))
    print("")
    return score


def cfr(game, position):

    if game.State == TERMINAL:
        if game.get_winner() == 2:
            return 0
        else:
            return game.Pots[1 - game.get_winner()]

    actions = game.get_legal_actions()

    if game.get_current_player() == position:
        action = input("Pick action from: {1} ".format(game.get_current_player(), actions))
        indices = []
        if action == "d":
            indices = [int(x) for x in input("Pick cards: ").split()]
    else:
        infoSet = str(game.Hands[1-position].to_string_simplified()) + game.History
        strat = strategy[infoSet]
        action, indices = get_action(actions, strat)
        print("Oppenent picked {0}".format(action))
        if action == "d":
            print(strat)
            print("Opponent picked cards: {0}".format(indices))

    game.perform_action(action, indices)

    return cfr(game, position)


play_game(0)
