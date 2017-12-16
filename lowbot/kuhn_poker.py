import time
import progressbar
import numpy as np


class KuhnTrainer(object):

    def __init__(self, iterations):
        self.PASS = 0
        self.BET = 1
        self.NUM_ACTIONS = 2
        self.nodeMap = {}
        self.iterations = iterations

    def createNode(self):
        return self.Node(self.NUM_ACTIONS)

    class Node(object):

        def __init__(self, NUM_ACTIONS):
            self.NUM_ACTIONS = NUM_ACTIONS
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
        cards = [i for i in range(13)]
        util = 0.

        bar = progressbar.ProgressBar(maxval=iterations, \
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for i in range(iterations):
            cards = np.random.permutation(cards)
            util += self.cfr(cards, "", 1, 1)
            bar.update(i + 1)

        print("Average game value: {0}, after {1} iterations.".format(util / iterations, iterations))

        for n in self.nodeMap.values():
            print(n.toString())


    def cfr(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history.endswith("bb")
            isPlayerCardHigher = cards[player] > cards[opponent]

            if terminalPass:
                if history == "pp":
                    return 1 if isPlayerCardHigher else -1
                else:
                    return 1
            elif doubleBet:
                return 2 if isPlayerCardHigher else -2

        infoSet = str(cards[player]) + history

        node = None
        if infoSet in self.nodeMap.keys():
            node = self.nodeMap[infoSet]
        else:
            node = self.createNode()
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node

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
