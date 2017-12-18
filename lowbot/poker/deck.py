#!/usr/bin/env python3

import numpy as np

NUM_CARDS = 13
NUM_SUITS = 4

class card(object):
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['c', 'd', 'h', 's']

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def toString(self):
        return self.values[self.value] + self.suits[self.suit]


class deck(object):

    def __init__(self):
        self.cards = []
        for s in range(NUM_SUITS):
            for v in range(NUM_CARDS):
                self.cards.append(card(v, s))


    def shuffle(self, seed=None):
        self.cards = list(np.random.RandomState(seed=seed).permutation(self.cards))

    def toString(self):
        s = ""
        for c in self.cards:
            s += c.toString() + ' '
        return s[0:len(s)-1]
