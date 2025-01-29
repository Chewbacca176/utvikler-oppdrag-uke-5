import random

g = {"a": [], "b": [], "c": [], "d": []}
for i in range(10):
    g["a"].append(random.randint(1, 11))
    g["b"].append(random.randint(1, 11))
    g["c"].append(random.randint(1, 11))
    g["d"].append(random.randint(1, 11))
   

print(g["a"][0])