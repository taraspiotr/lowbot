import random

# PURE_STRATEGIES = [[5, 0, 0], [0, 5, 0], [0, 0, 5],
#                   [4, 1, 0], [1, 4, 0], [1, 0, 4],
#                   [4, 0, 1], [0, 4, 1], [0, 1, 4],
#                   [3, 1, 1], [1, 3, 1], [1, 1, 3],
#                   [3, 2, 0], [2, 3, 0], [2, 0, 3],
#                   [3, 0, 2], [0, 3, 2], [0, 2, 3],
#                   [2, 2, 1], [2, 1, 2], [1, 2, 2]]

PURE_STRATEGIES = [[5, 0, 0], [0, 5, 0], [0, 0, 5],
                  [4, 1, 0], [1, 4, 0], [1, 0, 4],
                  [4, 0, 1], [0, 4, 1], [0, 1, 4],
                  [3, 1, 1], [1, 3, 1], [1, 1, 3],
                  [3, 2, 0], [2, 3, 0], [2, 0, 3],
                  [3, 0, 2], [0, 3, 2], [0, 2, 3],
                  [2, 2, 1], [2, 1, 2], [1, 2, 2]]

NUM_ACTIONS = len(PURE_STRATEGIES)

regretSum = [0.0 for i in range(NUM_ACTIONS)]
strategy = [0.0 for i in range(NUM_ACTIONS)]
strategySum = [0.0 for i in range(NUM_ACTIONS)]
oppStrategy = [0.3, 0.4, 0.3]
oppRegretSum = [0.0 for i in range(NUM_ACTIONS)]

def getStrategy(currRegretSum):
    normalizingSum = 0

    for a in range(NUM_ACTIONS):
        strategy[a] = currRegretSum[a] if currRegretSum[a] > 0 else 0
        normalizingSum += strategy[a]

    for a in range(NUM_ACTIONS):
        if normalizingSum > 0:
            strategy[a] /= normalizingSum
        else:
            strategy[a] = 1.0 / NUM_ACTIONS
        strategySum[a] += strategy[a]
    return strategy

def getAction(strategy):
    r = random.random()
    a = 0
    cumulativeProbability = 0
    while a < NUM_ACTIONS - 1:
        cumulativeProbability += strategy[a]
        if (r < cumulativeProbability):
            break
        a += 1
    return a


def getUtility(action):
    otherStrategy = PURE_STRATEGIES[action]

    actionUtility = [0 for i in range(NUM_ACTIONS)]

    for a in range(NUM_ACTIONS):
        myStrategy = PURE_STRATEGIES[a]
        myFields = 0
        for i in range(len(myStrategy)):
            if myStrategy[i] > otherStrategy[i]:
                myFields += 1
            elif myStrategy[i] < otherStrategy[i]:
                myFields -= 1

        if myFields > 0:
            actionUtility[a] = 1
        elif myFields < 0:
            actionUtility[a] = -1
        else:
            actionUtility[a] = 0

    return actionUtility

def train(iterations):
    for i in range(iterations):
        print(i)
        strategy = getStrategy(regretSum)
        myAction = getAction(strategy)
        oppStrategy = getStrategy(oppRegretSum)
        otherAction = getAction(oppStrategy)

        actionUtility = getUtility()

        for a in range(NUM_ACTIONS):
            regretSum[a] += actionUtility[a] - actionUtility[myAction]
            oppRegretSum[a] -= actionUtility[a] - actionUtility[otherAction]


        print(strategy)




def getAverageStrategy():
    avgStrategy = [0 for i in range(NUM_ACTIONS)]
    normalizingSum = 0
    for a in range(NUM_ACTIONS):
        normalizingSum += strategySum[a]
    for a in range(NUM_ACTIONS):
        if normalizingSum > 0:
            avgStrategy[a] = strategySum[a] / normalizingSum
        else:
            avgStrategy[a] = 1.0 / NUM_ACTIONS
    return avgStrategy


def main():
    train(1000000)
    print(getAverageStrategy())

main()
