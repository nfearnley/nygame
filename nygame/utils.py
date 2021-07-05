from itertools import cycle, chain

def clamp(minval, val, maxval):
    return max(minval, min(val, maxval))

def recycle(num):
    return cycle(chain(range(num), range(num-2, 0, -1)))
