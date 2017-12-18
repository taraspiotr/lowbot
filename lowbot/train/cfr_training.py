import random

ROCK = 0
PAPER = 1
SCISSORS = 2
NUM_ACTIONS = 3

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

def train(iterations):
    actionUtility = [0 for i in range(NUM_ACTIONS)]
    for i in range(iterations):
        print(i)
        strategy = getStrategy(regretSum)
        myAction = getAction(strategy)
        oppStrategy = getStrategy(oppRegretSum)
        otherAction = getAction(oppStrategy)

        actionUtility[otherAction] = 0
        actionUtility[0 if otherAction == NUM_ACTIONS - 1 else otherAction + 1] = 1
        actionUtility[NUM_ACTIONS - 1 if otherAction == 0 else otherAction - 1] = -1

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
    train(5000000)
    print(getAverageStrategy())

main()

