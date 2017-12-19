from lowbot.poker.deck import *
import operator

class Hand(object):

    def __init__(self, cards):
        self.Cards = cards
        self.Cards.sort(key=lambda x: (x.Value, x.Suit), reverse=True)
        self.HandValue = self._get_hand_value()
        self.Discarded = []

    def draw(self, indices, cards):
        for e, i in enumerate(indices):
            self.Discarded.append(self.Cards[i])
            self.Cards[i] = cards[e]

        self.Cards.sort(key=lambda x: (x.Value, x.Suit), reverse=True)

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
                return -1
        return 0

    def _get_hand_value(self):

        rank = self._is_royal_flush()
        if rank:
            return rank
        rank = self._is_straight_flush()
        if rank:
            return rank
        rank = self.is_four_of_a_kind()
        if rank:
            return rank
        rank = self._is_full_house()
        if rank:
            return rank
        rank = self._is_flush()
        if rank:
            return rank
        rank = self._is_straight()
        if rank:
            return rank
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
        for c in self.Cards:
            rank.append(c.Value)
        return rank


