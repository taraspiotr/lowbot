import time
import numpy as np
from lowbot.poker import poker
from lowbot.poker import razz


class KuhnTrainer(object):

    def __init__(self, iterations):
        self.PASS = 0
        self.BET = 1
        # self.NUM_ACTIONS = 2
        self.nodeMap = {}
        self.iterations = iterations

    def createNode(self, num_actions):
        return self.Node(num_actions)

    class Node(object):

        def __init__(self, num_actions):
            self.NUM_ACTIONS = num_actions
            self.infoSet = ""
            self.regretSum = np.zeros(self.NUM_ACTIONS)
            self.strategy = np.zeros(self.NUM_ACTIONS)
            self.strategySum = np.zeros(self.NUM_ACTIONS)

        def getStrategy(self, realizationWeight):
            normalizingSum = 0

            for a in range(self.NUM_ACTIONS):
                self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
                normalizingSum += self.strategy[a]

            for a in range(self.NUM_ACTIONS):
                if normalizingSum > 0:
                    self.strategy[a] /= normalizingSum
                else:
                    self.strategy[a] = 1.0 / self.NUM_ACTIONS

                self.strategySum[a] += realizationWeight * self.strategy[a]

            return self.strategy

        def getAverageStrategy(self):
            avgStrategy = np.zeros(self.NUM_ACTIONS)
            normalizingSum = 0

            for a in range(self.NUM_ACTIONS):
                normalizingSum += self.strategySum[a]

            for a in range(self.NUM_ACTIONS):
                if normalizingSum > 0:
                    avgStrategy[a] = self.strategySum[a] / normalizingSum
                else:
                    avgStrategy[a] = 1.0 / self.NUM_ACTIONS

            return avgStrategy

        def toString(self):
            return str.format("{0}:   \t[{1:.0f}%  \t{2:.0f}%]", self.infoSet, self.getAverageStrategy()[0]*100, self.getAverageStrategy()[1]*100)

    def train(self, iterations):
        deck = poker.Deck()
        util = 0.

        for i in range(iterations):
            deck.shuffle()
            cards = deck.to_string_simplified()
            util += self.cfr(cards, "", 1, 1)
            print("Iteration {0} / {1}".format(i, iterations))
        print("Average game value: {0}, after {1} iterations.".format(util / iterations, iterations))

        for n in self.nodeMap.values():
            print(n.toString())


    def cfr(self, cards, history, p0, p1):
        player = razz.get_current_player(history)
        opponent = 1 - player

        actions = razz.get_legal_actions(history)

        if actions == razz.TERMINAL_FOLD:
            return razz.get_pot_contribution(opponent)

        if actions == razz.TERMINAL_CALL:
            outcome = razz.compare_final_hands(history, hands[player], hands[opponent])
            if outcome == 0:
                return razz.get_pot_contribution(history, 0)
            if outcome == 1:
                return -razz.get_pot_contribution(history, 0)
            if outcome == 2:
                return 0

        if actions == razz.DRAW:
            history += "(" + cards.pop() + cards.pop()

        infoSet = str(cards[player]) + history

        node = None
        if infoSet in self.nodeMap.keys():
            node = self.nodeMap[infoSet]
        else:
            node = self.createNode()
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node


        if p0 + p1 < 1e-6:

            print(infoSet, p0, p1)
            return 0

        strategy = node.getStrategy(p0 if player == 0 else p1)
        util = np.zeros(self.NUM_ACTIONS)
        nodeUtil = 0.

        for a in range(self.NUM_ACTIONS):
            nextHistory = history + ("p" if a == 0 else "b")
            util[a] = -self.cfr(cards, nextHistory, p0 * strategy[a], p1) if player == 0 else -self.cfr(cards, nextHistory, p0, p1 * strategy[a])
            nodeUtil += strategy[a] * util[a]

        for a in range(self.NUM_ACTIONS):
            regret = util[a] - nodeUtil
            node.regretSum[a] += (p1 if player == 0 else p0) * regret

        return nodeUtil

    def main(self):
        self.train(self.iterations)

Trainer = KuhnTrainer(1000000)
Trainer.main()
