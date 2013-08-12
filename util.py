
def sgn(x):
    if x >= 0:
        return 1
    return -1

def distance(a, b):
    import math
    return math.sqrt((a.x - b.x) ** 2 + (a.z - b.z) ** 2)