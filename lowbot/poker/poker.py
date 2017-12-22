#!/usr/bin/env python3

import numpy as np
import operator

NUM_CARDS = 13
NUM_SUITS = 4
H = 1
L = 2
HL = 3


class Card(object):
    Values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
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


class Hand(object):

    def __init__(self, cards):
        self.Cards = cards
        self.Cards.sort(key=lambda x: (x.Value, x.Suit), reverse=True)
        self.HandValue = self._get_hand_value()

    def to_string(self):
        s = ""
        for c in self.Cards:
            s += c.to_string() + ' '
        return s[0:len(s)-1]

    def to_string_simplified(self):
        s = ""
        for c in self.Cards:
            s += c.to_string_simplified()
        return s

    def compare(self, second_hand):
        for i in range(min(len(self.HandValue), len(second_hand.HandValue))):
            if self.HandValue[i] > second_hand.HandValue[i]:
                return 1
            elif self.HandValue[i] < second_hand.HandValue[i]:
                return 0
        return 2

    def _get_hand_value(self):

        # rank = self._is_royal_flush()
        # if rank:
        #     return rank
        # rank = self._is_straight_flush()
        # if rank:
        #     return rank
        rank = self.is_four_of_a_kind()
        if rank:
            return rank
        rank = self._is_full_house()
        if rank:
            return rank
        # rank = self._is_flush()
        # if rank:
        #     return rank
        # rank = self._is_straight()
        # if rank:
        #     return rank
        rank = self._is_three_of_a_kind()
        if rank:
            return rank
        rank = self._is_two_pair()
        if rank:
            return rank
        rank = self._is_pair()
        if rank:
            return rank
        rank = self._is_high_card()
        if rank:
            return rank

        return None

    def _bucket_cards(self):
        buckets = {}
        for i in range(NUM_CARDS):
            buckets[i] = 0
        for c in self.Cards:
            buckets[c.Value] += 1
        return sorted(buckets.items(), key=operator.itemgetter(1))

    def _is_royal_flush(self):
        if len(self.Cards) < 5 or self.Cards[0].Value != 12:
            return None

        for i in range(1, 5):
            if self.Cards[i].Value != self.Cards[i-1].Value - 1 or self.Cards[i].Suit != self.Cards[i-1].Suit:
                return None

        return [10, self.Cards[0].Suit]

    def _is_straight_flush(self):
        if len(self.Cards) < 5:
            return None

        for i in range(1, 5):
            if self.Cards[i].Value != self.Cards[i-1].Value - 1 or self.Cards[i].Suit != self.Cards[i-1].Suit:
                return None

        return [9, self.Cards[0].Value, self.Cards[0].Suit]

    def is_four_of_a_kind(self):

        buckets = self._bucket_cards()
        if buckets[-1][1] != 4:
            return None

        return [8, buckets[-1][0]]

    def _is_full_house(self):

        buckets = self._bucket_cards()
        if buckets[-1][1] != 3 or buckets[-2][1] != 2:
            return None

        return [7, buckets[-1][0], buckets[-2][0]]

    def _is_flush(self):
        if len(self.Cards) < 5:
            return None

        for i in range(1, 5):
            if self.Cards[i].Suit != self.Cards[i-1].Suit:
                return None

        return [6, self.Cards[0].Value, self.Cards[0].Suit]

    def _is_straight(self):
        if len(self.Cards) < 5:
            return None

        for i in range(1, 5):
            if self.Cards[i].Value != self.Cards[i-1].Value - 1:
                return None

        return [5, self.Cards[0].Value]

    def _is_three_of_a_kind(self):

        buckets = self._bucket_cards()
        if buckets[-1][1] != 3:
            return None

        rank = [4, buckets[-1][0]]
        if len(self.Cards) >= 4:
            rank.append(buckets[-2][0])
        if len(self.Cards) >= 5:
            rank.append(buckets[-3][0])

        return rank

    def _is_two_pair(self):

        buckets = self._bucket_cards()
        if buckets[-1][1] != 2 or buckets[-2][1] != 2:
            return None

        rank = [3, buckets[-1][0], buckets[-2][0]]

        if len(self.Cards) >= 5:
            rank.append(buckets[-3][0])

        return rank

    def _is_pair(self):

        buckets = self._bucket_cards()
        if buckets[-1][1] != 2:
            return None

        rank = [2, buckets[-1][0]]
        if len(self.Cards) >= 3:
            rank.append(buckets[-2][0])
        if len(self.Cards) >= 4:
            rank.append(buckets[-3][0])
        if len(self.Cards) >= 5:
            rank.append(buckets[-4][0])

        return rank

    def _is_high_card(self):

        rank = [1]
        flag_ace = True if self.Cards[0].Value == 12 else False

        if flag_ace:
            for c in self.Cards[1:]:
                rank.append(c.Value)
            rank.append(-1)
        else:
            for c in self.Cards:
                rank.append(c.Value)
        return rank


