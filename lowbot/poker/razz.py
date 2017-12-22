import re

History = "(K8)crrc(A3)cc(65)crc(44)crrc()sa"

s = re.findall('\(([^)]+)', History)
a = re.findall('\)([^(]+)', History)
print(s)

NUM_CARDS = 13
NUM_SUITS = 4

VALUES_LOW = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13}
VALUES_HIGH = {'A':14, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13}
SUITS = {'c':1, 'd':2, 'h':3, 's':4}

def compare_hands(hand_one, hand_two, low=False, suit=False):
    if suit:
        hand_one =
