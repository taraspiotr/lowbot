import re
from lowbot.poker import poker
import itertools

VALUES = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
SUITS = {'c':0, 'd':1, 'h':2, 's':3}
DRAW = "DRAW"
LAST_DRAW = "LAST_DRAW"
TERMINAL_FOLD = "TERMINAL_FOLD"
TERMINAL_CALL = "TERMINAL_CALL"
ONGOING = "ONGOING"
CAP = 3
NUM_DRAWS = 3
NUM_CARDS = 5
SMALL_BET = 1
BIG_BET = 2


def get_legal_actions(history):
    rounds = re.findall(r'([^[\)]+)(?:$|\()', history)
    draws = re.findall(r'([^[\(]+)(?:$|\))', history)

    if len(history) == 0 or history[-1] == ")":
        return "fcr"

    last_round = rounds[-1]
    plays = len(last_round)

    if last_round.count("("):
        return LAST_DRAW

    if last_round[-1] == "f":
        return TERMINAL_FOLD

    if len(rounds) == 1 and last_round == "rc":
        return "fcr"

    if plays > 1:
        if last_round[-1] == "c":
            if len(draws) < NUM_DRAWS:
                return DRAW
            else:
                return TERMINAL_CALL
        if last_round[-1] == "r":
            if last_round.count("r") < CAP:
                return "fcr"
            else:
                return "fc"

    return "fcr"


def get_current_player(history):
    rounds = re.findall(r'([^[\)]+)(?:$|\()', history)
    draws = re.findall(r'([^[\(]+)(?:$|\))', history)

    if len(history) == 0 or history[-1] == ")":
        return 1

    last_round = rounds[-1]
    plays = len(last_round)

    if last_round.count("("):
        return 0

    if plays > 1 and last_round[-1] == "c":
        return 1

    return 1 - len(last_round) % 2


