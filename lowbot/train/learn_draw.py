import time
import numpy as np
from lowbot.poker import poker
from lowbot.poker import draw


class KuhnTrainer(object):

    def __init__(self, iterations):
        self.PASS = 0
        self.BET = 1
        # self.NUM_ACTIONS = 2
        self.nodeMap = {}
        self.iterations = iterations

    def createNode(self, num_actions, actions):
        return self.Node(num_actions, actions)

    class Node(object):

        def __init__(self, num_actions, actions):
            self.NUM_ACTIONS = num_actions
            self.actions = actions
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
            return str.format("{0}:\t{1}", self.infoSet, self.getAverageStrategy())

        def toCSV(self):
            return str.format("{0},{1}", self.infoSet, ",".join(map(str, self.getAverageStrategy())))

    def train(self, iterations):
        deck = poker.Deck()
        util = 0.

        try:
            for i in range(iterations):
                deck.shuffle()
                cards = deck.to_string_simplified()
                hand_one = draw.sort_cards(cards[0:draw.NUM_CARDS])
                hand_two = draw.sort_cards(cards[draw.NUM_CARDS:2 * draw.NUM_CARDS])
                util += self.cfr(cards, "r", hand_one, hand_two, 1, 1)
                print("Iteration {0} / {1}".format(i, iterations))
        except KeyboardInterrupt:
            pass

        print("Average game value: {0}, after {1} iterations.".format(util / iterations, iterations))

        with open("strategy.csv", "w") as f:
            for n in self.nodeMap.values():
                # print(n.toString())
                f.write(n.toCSV() + "\n")

    def cfr(self, cards, history, hand_one, hand_two, p0, p1):
        # print("\t", history)
        player = draw.get_current_player(history)
        opponent = 1 - player
        player_hand = hand_one if player == 0 else hand_two
        opponent_hand = hand_one if opponent == 0 else hand_two

        actions = draw.get_legal_actions(history)

        # print(history)
        # print(actions)
        # print("")

        if actions == draw.TERMINAL_FOLD:
            return draw.get_pot_contribution(history, opponent)

        if actions == draw.TERMINAL_CALL:
            outcome = draw.compare_hands(player_hand, opponent_hand)
            if outcome == 0:
                return draw.get_pot_contribution(history, 0)
            if outcome == 1:
                return -draw.get_pot_contribution(history, 0)
            if outcome == 2:
                return 0

        # if actions == razz.DRAW:
        #     history += "(" + razz.get_draw_cards(history, cards) + ")"
        #     return self.cfr(cards, history, p0, p1)
        # if actions == razz.DRAW_FACE_DOWN:
        #     history += "()"
        #     return self.cfr(cards, history, p0, p1)

        infoSet = player_hand + history

        node = None
        if infoSet in self.nodeMap.keys():
            node = self.nodeMap[infoSet]
        else:
            if actions == draw.DRAW or actions == draw.LAST_DRAW:
                node = self.createNode(2**draw.NUM_CARDS, actions)
            else:
                node = self.createNode(len(actions), actions)
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node


        # if p0 + p1 < 1e-6:
        #
        #     print(infoSet, p0, p1)
        #     return 0

        strategy = node.getStrategy(p0 if player == 0 else p1)
        util = np.zeros(node.NUM_ACTIONS)
        nodeUtil = 0.

        for a in range(node.NUM_ACTIONS):
            if actions == draw.DRAW or actions == draw.LAST_DRAW:
                num_drawed, new_hand = draw.draw_cards(history, cards, player_hand, a)
                if actions == draw.DRAW:
                    nextHistory = history + "(" + str(num_drawed)
                else:
                    nextHistory = history + str(num_drawed) + ")"
            else:
                nextHistory = history + node.actions[a]
                new_hand = player_hand
            util[a] = -self.cfr(cards, nextHistory, new_hand, opponent_hand, p0 * strategy[a], p1) if player == 0 else -self.cfr(cards, nextHistory, opponent_hand, new_hand, p0, p1 * strategy[a])
            nodeUtil += strategy[a] * util[a]

        for a in range(node.NUM_ACTIONS):
            regret = util[a] - nodeUtil
            node.regretSum[a] += (p1 if player == 0 else p0) * regret

        return nodeUtil

    def main(self):
        self.train(self.iterations)

Trainer = KuhnTrainer(1000)
Trainer.main()
