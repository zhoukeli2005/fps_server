
def sgn(x):
    if x >= 0:
        return 1
    return -1

def distance(a, b):
    import math
    return math.sqrt((a.x - b.x) ** 2 + (a.z - b.z) ** 2)

def normalize(x, z):
    import math
    L = math.sqrt(x ** 2 + z ** 2)
    if L <= 0:
        L = 1
    return x / L, z / L