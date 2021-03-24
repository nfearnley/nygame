from typing import Generic, List, TypeVar, Union

from bisect import bisect_left, bisect_right


class Coord:
    def __init__(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)

    @xy.setter
    def xy(self, value):
        self.x, self.y = value

    def __getitem__(self, key):
        return self.xy[key]

    def __setitem__(self, key, value):
        setattr(self, ("x", "y")[key], value)

    def __iter__(self):
        return iter(self.xy)

    def __add__(self, other):
        ax, ay = self
        bx, by = other
        return Coord(ax + bx, ay + by)

    __radd__ = __add__

    def __iadd__(self, other):
        self.xy = self + other
        return self

    def __sub__(self, other):
        ax, ay = self
        bx, by = other
        return Coord(ax - bx, ay - by)

    def __rsub__(self, other):
        ax, ay = other
        bx, by = self
        return Coord(ax - bx, ay - by)

    def __isub__(self, other):
        self.xy = self - other
        return self

    def __mul__(self, other):
        """Coord(2, 3) * 4 == Coord(8, 12)"""
        x, y = self
        return Coord(x * other, y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        self.xy = self * other
        return self

    def __truediv__(self, other):
        return self * (1 / other)

    def __itruediv__(self, other):
        self.xy = self / other
        return self

    def __eq__(self, other):
        return self.xy == other

    def __str__(self):
        return str(self.xy)

    def __repr__(self):
        return f"<Coord({self.x}, {self.y})>"

    def __len__(self):
        return 2


T = TypeVar("T")
K = TypeVar("K")


class Index(Generic[K, T]):
    """
    Class to provide efficient indexing and slicing operations into a list of objects by certain attribute key.

    This with *only* work if:
    - The list is sorted
    - The list doesn't change

    I have not tested how this will handle duplicate values.
    """

    def __init__(self, items: List[T], keyattr: str):
        self.items = items
        self.keys: List[K] = [getattr(i, keyattr) for i in items]

    def __getitem__(self, key: Union[slice, K]) -> Union[None, T]:
        if isinstance(key, slice):
            start_index, stop_index = find_index_range(self.keys, key.start, key.stop)
            return self.items[start_index:stop_index:key.step]
        else:
            index = find_index(self.keys, key)
            if index is None:
                return None
            return self.items[index]

    def index(self, key: K) -> int:
        return find_index(self.keys, key)


def find_index(keys: List[T], value: T) -> Union[None, int]:
    index = bisect_right(keys, value) - 1
    if index < 0:
        index = None
    return index


def find_index_range(keys: List[T], start: T, stop: T) -> int:
    start_index = None if start is None else bisect_left(keys, start)
    stop_index = None if stop is None else bisect_left(keys, stop)
    return start_index, stop_index
