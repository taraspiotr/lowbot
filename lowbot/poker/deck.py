#!/usr/bin/env python3

import numpy as np

NUM_CARDS = 13
NUM_SUITS = 4

class Card(object):
    Values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    Suits = ['c', 'd', 'h', 's']

    def __init__(self, value, suit):
        self.Value = value
        self.Suit = suit

    def to_string(self):
        return self.Values[self.Value] + self.Suits[self.Suit]

    def to_string_simplified(self):
        return self.Values[self.Value]

class Deck(object):

    def __init__(self, num_suits=4, num_cards=13):
        self.Cards = []
        for s in range(num_suits):
            for v in range(num_cards):
                self.Cards.append(Card(v, s))


    def shuffle(self, seed=None):
        self.Cards = list(np.random.RandomState(seed=seed).permutation(self.Cards))

    def to_string(self):
        s = ""
        for c in self.Cards:
            s += c.to_string() + ' '
        return s[0:len(s)-1]
