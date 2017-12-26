

def one(q):
    print(q)
    print(two(q))
    print(two(q))
    print(two(q))
    print(two(q))


def two(q):
    q = [q[0] + "a", q[1]]
    return q

one(["s", "b"])
