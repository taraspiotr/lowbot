from train.game import *
import copy


class KuhnTrainer(object):

    def __init__(self, iterations):
        self.PASS = 0
        self.BET = 1
        self.NUM_CARDS = 1
        self.nodeMap = {}
        self.iterations = iterations

    def createNode(self, actions):
        return self.Node(actions, self.NUM_CARDS)

    class Node(object):

        def __init__(self, actions, num_cards):
            if actions == "d":
                self.NUM_ACTIONS = 2**num_cards
            else:
                self.NUM_ACTIONS = len(actions)
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
            return str.format("{0} ({1}):\t{2}", self.infoSet, self.counter, self.getAverageStrategy())

        def toCSV(self):
            return str.format("{0},{1},{2}", self.infoSet, self.counter, ",".join(map(str, self.getAverageStrategy())))

    def train(self, iterations):
        util = 0.

        try:

            for i in range(iterations):
                game = Game(num_draws=0, hand_size=2, num_cards=13, cap=3, num_suits=4)
                util += self.cfr(game, 1, 1)
                del game
                print("Iteration {0} / {1}".format(i, iterations))
        except KeyboardInterrupt:
            pass

        print("Average game value: {0}, after {1} iterations.".format(util / iterations, iterations))

        with open("strategy.csv", "w") as f:
            for n in self.nodeMap.values():
                print(n.toString())
                f.write(n.toCSV() + "\n")


    def cfr(self, game, p0, p1):
        player = game.get_current_player()

        if game.State == TERMINAL:
            winner = game.get_winner()
            if winner == 2:
                return 0
            elif winner == player:
                return game.Pots[1 - winner]
            else:
                return -game.Pots[winner]

        infoSet = game.Hands[player].OldCards + str(game.Hands[player].to_string_simplified()) + game.History
        actions = game.get_legal_actions()

        if infoSet in self.nodeMap.keys():
            node = self.nodeMap[infoSet]
            self.nodeMap[infoSet].counter += 1
        else:
            node = self.createNode(actions)
            node.infoSet = infoSet
            self.nodeMap[infoSet] = node
            # if actions == "d":
            #     print(node.toString())
            #     print(node.NUM_ACTIONS)

        weight = p0 if player == 0 else p1
        # if p0 + p1 < 1e-6:
        #     node.counter -= 1e6

        strategy = node.getStrategy(weight)
        util = np.zeros(node.NUM_ACTIONS)
        nodeUtil = 0.

        for a in range(node.NUM_ACTIONS):
            game_copy = copy.deepcopy(game)
            indices = []

            if actions == "d":
                action = "d"
                for i, c in enumerate(format(a, '01b')):
                    if c == "1":
                        indices.append(i)

            else:
                action = actions[a]

            #print("Action = {0}, indices = {1}".format(action, indices))
            # print("\nPre action:")
            # print("\tHistory:\t{0}".format(game_copy.History))
            # print("\tHand 0: \t{0}".format(game_copy.Hands[0].to_string()))
            # print("\tHand 1: \t{0}".format(game_copy.Hands[1].to_string()))
            # print("\tState:  \t{0}".format(game_copy.State))
            # print("\tACTION: \t{0}, {1}".format(action, indices))
            game_copy.perform_action(action, indices)
            # print("Post action:")
            # print("\tHistory:\t{0}".format(game_copy.History))
            # print("\tHand 0: \t{0}".format(game_copy.Hands[0].to_string()))
            # print("\tHand 1: \t{0}".format(game_copy.Hands[1].to_string()))
            # print("\tState:  \t{0}".format(game_copy.State))

            util[a] = -self.cfr(game_copy, p0 * strategy[a], p1) if player == 0 else -self.cfr(game_copy, p0, p1 * strategy[a])
            nodeUtil += strategy[a] * util[a]
            del game_copy

        for a in range(node.NUM_ACTIONS):
            regret = util[a] - nodeUtil
            node.regretSum[a] += (p1 if player == 0 else p0) * regret

        return nodeUtil



    def main(self):
        self.train(self.iterations)

Trainer = KuhnTrainer(int(1e9))
Trainer.main()
