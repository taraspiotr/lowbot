import re
from lowbot.poker import poker
import itertools

History = "(K8)crrc(A3)cc(65)crc(44)crrc()sa"
#
# s = re.findall('\(([^)]+)', History)
# a = re.findall('\)([^(]+)', History)
# print(s)

VALUES = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
SUITS = {'c':0, 'd':1, 'h':2, 's':3}
DRAW = 100
TERMINAL = 111
ONGOING = 112
CAP = 113
NUM_BETTING = 5

def compare_hands(hand_one, hand_two):

    hand_one = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_one])
    hand_two = poker.Hand([poker.Card(VALUES[s], 0) for s in hand_two])

    return hand_one.compare(hand_two)

def get_hands_from_history(history):
    hands = re.findall('\(([^)]+)', history)
    hand_one = "".join([s[0] for s in hands])
    hand_two = "".join([s[1] for s in hands])

    return [hand_one, hand_two]

def get_legal_actions(history):
    rounds = re.findall('\)([^(]+)', history)

    if history[-1] == ")":
        return "fcr"

    plays = len(rounds[-1])

    if


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

h = "(8T)asdf(A6)cddr"
# print(get_current_player(h))

h1 = "AA5Q3"
h2 = "5K36A"

print(compare_final_hands(h, h1, h2))

# h1 = "A8"
# h2 = "76"
# print(compare_hands(h1, h2))
