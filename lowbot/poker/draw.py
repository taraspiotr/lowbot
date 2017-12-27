import re
from lowbot.poker import poker
import itertools

VALUES = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
VALUE_SIGNS = {0:'2', 1:'3', 2:'4', 3:'5', 4:'6', 5:'7', 6:'8', 7:'9', 8:'T', 9:'J', 10:'Q', 11:'K', 12:'A'}
SUITS = {'c':0, 'd':1, 'h':2, 's':3}
DRAW = "DRAW"
LAST_DRAW = "LAST_DRAW"
TERMINAL_FOLD = "TERMINAL_FOLD"
TERMINAL_CALL = "TERMINAL_CALL"
ONGOING = "ONGOING"
CAP = 2
NUM_DRAWS = 1
SB_ROUNDS = 2
NUM_CARDS = 1
SMALL_BET = 1
BIG_BET = 2


def get_legal_actions(history):
    rounds = re.findall(r'([^[\)]+)(?:$|\()', history)
    draws = re.findall('\(([^)]+)', history)

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
    action = get_legal_actions(history)

    if len(history) == 0 or history[-1] == ")":
        return 1

    last_round = rounds[-1]
    plays = len(last_round)

    if last_round.count("("):
        return 0

    if plays > 1 and last_round[-1] == "c" and (action == DRAW or action == LAST_DRAW):
        return 1

    return 1 - len(last_round) % 2


def compare_hands(hand_one, hand_two):

    hand_one = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_one[-NUM_CARDS:]], "DRAW")
    hand_two = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_two[-NUM_CARDS:]], "DRAW")

    return hand_one.compare(hand_two)


def sort_cards(hand):
    hand = [VALUES[s] for s in hand]
    hand.sort(reverse=True)
    hand = "".join([VALUE_SIGNS[a] for a in hand])
    # print(hand)
    return hand


def draw_cards(history, cards, hand, action):
    # draws = re.findall(r'([^[\(]+)(?:$|\))', history)
    draws = re.findall('\(([^)]+)', history)
    p = 2*NUM_CARDS
    # print("OLD", hand)
    for s in "".join(draws):
        p += int(s)

    action = format(action, '0' + str(NUM_CARDS) + 'b')
    hand_old = hand[:-NUM_CARDS]
    hand_last = hand[-NUM_CARDS:]

    hand_new = ""
    hand = ""

    for i, s in enumerate(hand_last):
        if action[i] == "0":
            hand_new += s
            hand += s
        else:
            hand_new += cards[p]
            p += 1
            hand += s#"+" + s

    hand_new = sort_cards(hand_new)
    hand = hand_old + hand + hand_new
    # print("NEW", hand)

    return action.count("1"), hand

def get_pot_contribution(history, player):
    rounds = re.findall(r'([^[\)]+)(?:$|\()', history)
    if len(rounds) == 1 and rounds[0] == "rf" and player == 0:
        return SMALL_BET / 2
    if len(rounds) == 1 and rounds[0] == "rcf" and player == 1:
        return SMALL_BET

    pot = 0

    for i, round in enumerate(rounds):
        if i < SB_ROUNDS:
            round_pot = round.count("r") * SMALL_BET
            if i == len(rounds) - 1 and rounds[-1][-1] == "f" and player == len(rounds[-1]) % 2 and round_pot > 0:
                round_pot -= SMALL_BET
        else:
            round_pot = round.count("r") * BIG_BET
            if i == len(rounds) - 1 and rounds[-1][-1] == "f" and player == len(rounds[-1]) % 2 and round_pot > 0:
                round_pot -= BIG_BET
        pot += round_pot

    return pot

def create_info_set(history, hand):
    info_set = hand[:NUM_CARDS]
    h = NUM_CARDS
    p = 0
    num_hands = len(hand) / NUM_CARDS

    while p < len(history):
        info_set += history[p]
        if history[p] == ")" and h < len(hand):
            info_set += hand[h:h+NUM_CARDS]
            h += NUM_CARDS
        p += 1

    return info_set


# cards="A25KQ96872AK48738TQ8K8A732"
# hand = "KJ954"
# history = "rcrc(12)rc(2"
# draw_cards(history, cards, hand, 24)
# print(draw_cards(history, cards, hand, 24))
# print(get_pot_contribution(history, 0))
# hand1 = "1234123422"
# hand2 = "41234123432"
# print(compare_hands(hand1, hand2))
# print(get_pot_contribution("rf", 0))
# print(get_legal_actions("rf"))
# print(get_current_player("rf"))
print(get_pot_contribution("rcrc", 0))
