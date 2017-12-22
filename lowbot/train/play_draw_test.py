import random
from train.game import *

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
        for i, c in enumerate(format(a, '02b')):
            if c == "1":
                indices.append(i)
        action = "d"
    else:
        action = actions[a]

    return [action, indices]


def play_game(position):
    game = Game(num_draws=0, hand_size=2, num_cards=13, cap=3, num_suits=4)
    if position == 0:
        print("You're on the SB")
    else:
        print("Your're on the BB")
    print("Your cards are {0}".format(game.Hands[position].to_string()))
    score = cfr(game, position)
    print("Your cards are {0}".format(game.Hands[position].to_string()))
    print("Opponent card are {0}".format(game.Hands[1-position].to_string()))
    print("Your score is {0}".format(score))
    print("")
    return score


def cfr(game, position):
    player = game.get_current_player()

    if game.State == TERMINAL:
        winner = game.get_winner()
        if winner == 2:
            return 0
        elif winner == position:
            return game.Pots[1 - position]
        else:
            return -game.Pots[position]

    actions = game.get_legal_actions()

    flag = False
    if player == position:
        action = input("Pick action from: {1} ".format(player, actions))
        # action = actions[random.randint(0, len(actions) - 1)]

        indices = []
        if action == "d":
            indices = [int(x) for x in input("Pick cards: ").split()]
            flag = True
    else:
        infoSet = game.Hands[1-position].OldCards + str(game.Hands[1-position].to_string_simplified()) + game.History
        strat = strategy[infoSet]
        action, indices = get_action(actions, strat)
        print("Oppenent picked {0} from {1}".format(action, actions))
        print(strat)
        if action == "d":
            print("Opponent picked cards: {0}".format(indices))

    game.perform_action(action, indices)

    if flag:
        print("Your new hand is: {0}".format(game.Hands[player].to_string()))


    return cfr(game, position)

while True:
    game_num += 1
    my_score += play_game(game_num%2)
    print("Total score is {0} after {1} games".format(my_score, game_num))
