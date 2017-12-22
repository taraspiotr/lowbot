
from collections import deque

q = deque()

q.append(1)
q.append(2)
q.append(3)
q.append(4)
q.append(5)
q.append(6)

def one(q):
    print("A: ", q.pop())
    two(q)
    two(q)

def two(q):
    print(q.pop())

one(q)
