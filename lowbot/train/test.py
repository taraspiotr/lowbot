
indices = []
a = 2
for i, c in enumerate(format(a, '02b')):
    if c == "1":
        indices.append(i)
print(indices)
