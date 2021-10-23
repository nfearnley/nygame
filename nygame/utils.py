from itertools import cycle, chain
from typing import TypeVar, Iterable

T = TypeVar("T", float, int)


def clamp(minval: T, val: T, maxval: T) -> T:
    return max(minval, min(val, maxval))


def recycle(num: int) -> Iterable[int]:
    return cycle(chain(range(num), range(num - 2, 0, -1)))
