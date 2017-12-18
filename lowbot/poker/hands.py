from poker.deck import *
import numpy as np
import operator

class hand(object):

    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(key=lambda x: (x.value, x.suit), reverse=True)
        self.handValue = self.getHandValue()

    def toString(self):
        s = ""
        for c in self.cards:
            s += c.toString() + ' '
        return s[0:len(s)-1]

    def compare(self, secondHand):
        for i in range(min(len(self.handValue), len(secondHand.handValue))):
            if self.handValue[i] > secondHand.handValue[i]:
                return 1
            elif self.handValue[i] < secondHand.handValue[i]:
                return -1
        return 0

    def getHandValue(self):

        rank = self.isRoyalFlush(self.cards)
        if rank:
            return rank
        rank = self.isStraightFlush(self.cards)
        if rank:
            return rank
        rank = self.isFourOfAKind(self.cards)
        if rank:
            return rank
        rank = self.isFullHouse(self.cards)
        if rank:
            return rank
        rank = self.isFlush(self.cards)
        if rank:
            return rank
        rank = self.isStraight(self.cards)
        if rank:
            return rank
        rank = self.isThreeOfAKind(self.cards)
        if rank:
            return rank
        rank = self.isTwoPair(self.cards)
        if rank:
            return rank
        rank = self.isPair(self.cards)
        if rank:
            return rank
        rank = self.isHighCard(self.cards)
        if rank:
            return rank

        return None

    def bucketCards(self, cards):
        buckets = {}
        for i in range(NUM_CARDS):
            buckets[i] = 0
        for c in cards:
            buckets[c.value] += 1
        return sorted(buckets.items(), key=operator.itemgetter(1))

    def isRoyalFlush(self, cards):
        if len(cards) < 5 or cards[0].value != 12:
            return None

        for i in range(1, 5):
            if cards[i].value != cards[i-1].value - 1 or cards[i].suit != cards[i-1].suit:
                return None

        return [10, cards[0].suit]

    def isStraightFlush(self, cards):
        if len(cards) < 5:
            return None

        for i in range(1, 5):
            if cards[i].value != cards[i-1].value - 1 or cards[i].suit != cards[i-1].suit:
                return None

        return [9, cards[0].value, cards[0].suit]

    def isFourOfAKind(self, cards):

        buckets = self.bucketCards(cards)
        if buckets[-1][1] != 4:
            return None

        return [8, buckets[-1][0]]

    def isFullHouse(self, cards):

        buckets = self.bucketCards(cards)
        if buckets[-1][1] != 3 or buckets[-2][1] != 2:
            return None

        return [7, buckets[-1][0], buckets[-2][0]]

    def isFlush(self, cards):
        if len(cards) < 5:
            return None

        for i in range(1, 5):
            if cards[i].suit != cards[i-1].suit:
                return None

        return [6, cards[0].value, cards[0].suit]

    def isStraight(self, cards):
        if len(cards) < 5:
            return None

        for i in range(1, 5):
            if cards[i].value != cards[i-1].value - 1:
                return None

        return [5, cards[0].value]

    def isThreeOfAKind(self, cards):

        buckets = self.bucketCards(cards)
        if buckets[-1][1] != 3:
            return None

        rank = [4, buckets[-1][0]]
        if len(cards) >= 4:
            rank.append(buckets[-2][0])
        if len(cards) >= 5:
            rank.append(buckets[-3][0])

        return rank

    def isTwoPair(self, cards):

        buckets = self.bucketCards(cards)
        if buckets[-1][1] != 2 or buckets[-2][1] != 2:
            return None

        rank = [3, buckets[-1][0], buckets[-2][0]]

        if len(cards) >= 5:
            rank.append(buckets[-3][0])

        return rank

    def isPair(self, cards):

        buckets = self.bucketCards(cards)
        if buckets[-1][1] != 2:
            return None

        rank = [2, buckets[-1][0]]
        if len(cards) >= 3:
            rank.append(buckets[-2][0])
        if len(cards) >= 4:
            rank.append(buckets[-3][0])
        if len(cards) >= 5:
            rank.append(buckets[-4][0])

        return rank

    def isHighCard(self, cards):

        rank = [1]
        for c in cards:
            rank.append(c.value)
        return rank
