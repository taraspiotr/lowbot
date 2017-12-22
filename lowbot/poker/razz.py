import re
from lowbot.poker import poker
import itertools

VALUES = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
SUITS = {'c':0, 'd':1, 'h':2, 's':3}
DRAW = "DRAW"
DRAW_FACE_DOWN = "DRAW_FACE_DOWN"
TERMINAL_FOLD = "TERMINAL_FOLD"
TERMINAL_CALL = "TERMINAL_CALL"
ONGOING = "ONGOING"
CAP = 4
NUM_BETTING = 5
BB_ROUND = 3
ANTE = 0.25
SMALL_BET = 1
BIG_BET = 2


def compare_hands(hand_one, hand_two):

    hand_one = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_one])
    hand_two = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_two])

    return hand_one.compare(hand_two)

def get_private_hands(history, cards):
    pass

def get_hands_from_history(history):
    hands = re.findall('\(([^)]+)', history)
    hand_one = "".join([s[0] for s in hands])
    hand_two = "".join([s[1] for s in hands])

    return [hand_one, hand_two]


def get_pot_contribution(history, player):
    rounds = re.findall('\)([^(]+)', history)
    hands = re.findall('\(([^)]+)', history)

    pot = ANTE
    temp_history = ""

    for i, current_round in enumerate(rounds):
        temp_history += "(" + hands[i] + ")"
        first_player = get_current_player(temp_history)

        r_count = current_round.count("r")

        if current_round[-1] == "f":
            if (first_player == player and len(current_round) % 2 == 1) or (first_player != player and len(current_round) % 2 == 0):
                r_count -= 1

        if i + 1 < BB_ROUND:
            round_pot = r_count * SMALL_BET
        else:
            round_pot = r_count * BIG_BET

        if i == 0 and player != first_player and round_pot == 0:
            round_pot = ANTE

        pot += round_pot

    return pot


def get_legal_actions(history):
    rounds = re.findall('\)([^(]+)', history)

    if history[-1] == ")":
        if len(rounds) == 0:
            return "fr"
        else:
            return "fcr"

    last_round = rounds[-1]
    plays = len(last_round)

    if last_round[-1] == "f":
        return TERMINAL_FOLD

    if plays > 1:
        if last_round[-1] == "c":
            if len(rounds) < NUM_BETTING:
                if len(round() == NUM_BETTING - 1):
                    return DRAW_FACE_DOWN
                else:
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
    hands = get_hands_from_history(history)
    rounds = re.findall('\)([^(]+)', history)

    if history[-1] == ")":
        rounds.append("")

    # if len(rounds) == 1:
    #     starter = 1 - compare_hands(hands[0], hands[1])
    # else:
    starter = compare_hands(hands[0], hands[1])

    return (starter + len(rounds[-1])) % 2


def get_final_hand(history, private_cards, player):

    return private_cards + get_hands_from_history(history)[player]


def compare_final_hands(history, private_one, private_two):

    cards_one = get_final_hand(history, private_one, 0)
    cards_two = get_final_hand(history, private_two, 1)
    print(cards_one, cards_two)
    if len(cards_one) > 5:
        best_one = cards_one[:5]
        for s in itertools.combinations(cards_one, 5):
            temp_hand = "".join(s)
            if compare_hands(best_one, temp_hand) == 1:
                best_one = temp_hand
    else:
        best_one = cards_one

    if len(cards_two) > 5:
        best_two = cards_two[:5]
        for s in itertools.combinations(cards_two, 5):
            temp_hand = "".join(s)
            if compare_hands(best_two, temp_hand) == 1:
                best_two = temp_hand
    else:
        best_two = cards_two
    print(best_one, best_two)
    return compare_hands(best_one, best_two)
