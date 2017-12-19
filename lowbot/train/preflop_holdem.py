from lowbot.poker.deck import *
from lowbot.poker.hands import Hand


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
            self.counter = 1

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
            return str.format("{0} ({1}):\t[{2:.0f}%\t{3:.0f}%]", self.infoSet, self.counter, self.getAverageStrategy()[0]*100, self.getAverageStrategy()[1]*100)

        def toCSV(self):
            return str.format("{0}, {1}", self.infoSet, self.getAverageStrategy()[0])

    def train(self, iterations):
        cards = Deck()
        util = 0.


        for i in range(iterations):
            cards.shuffle()
            util += self.cfr(cards, "", 1, 1)
            print("Iteration {0} / {1}".format(i, iterations))

        print("Average game value: {0}, after {1} iterations.".format(util / iterations, iterations))

        with open("strategy.csv", "w") as f:
            for n in self.nodeMap.values():
                print(n.toString())
                f.write(n.toCSV() + "\n")


    def cfr(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player
        hands = [Hand(cards.Cards[0:2]), Hand(cards.Cards[2:4])]
        playerHand = hands[player]
        oppHand = hands[opponent]

        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history.endswith("bb")
            isPlayerCardHigher = playerHand.compare(oppHand)

            if terminalPass:
                if history == "pp":
                    return isPlayerCardHigher
                else:
                    return 1
            elif doubleBet:
                return 2*isPlayerCardHigher

        infoSet = str(playerHand.to_string_simplified()) + history

        node = None
        if infoSet in self.nodeMap.keys():
            node = self.nodeMap[infoSet]
            self.nodeMap[infoSet].counter += 1
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

Trainer = KuhnTrainer(100000)
Trainer.main()
