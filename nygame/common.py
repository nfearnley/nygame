from typing import Generic, Sequence, Tuple, TypeVar, Union

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

    def __init__(self, items: Sequence[T], keyattr: str):
        self.items = items
        self.keys: Tuple[K] = tuple(getattr(i, keyattr) for i in items)

    def __getitem__(self, key: Union[slice, K]) -> T:
        if not isinstance(key, slice):
            return self.eq(key)

        start_index = key.start
        if start_index is not None:
            start_index = self.gteq_index(start_index)
            if start_index is None:
                return []

        stop_index = key.stop
        if stop_index is not None:
            stop_index = self.gteq_index(stop_index)

        return self.items[start_index:stop_index:key.step]

    def eq(self, key: K) -> T:
        index = self.eq_index(key)
        if index is None:
            return None
        return self.items[index]

    def lteq(self, key: K) -> T:
        index = self.lteq_index(key)
        if index is None:
            return None
        return self.items[index]

    def lt(self, key: K) -> T:
        index = self.lt_index(key)
        if index is None:
            return None
        return self.items[index]

    def gteq(self, key: K) -> T:
        index = self.gteq_index(key)
        if index is None:
            return None
        return self.items[index]

    def gt(self, key: K) -> T:
        index = self.gt_index(key)
        if index is None:
            return None
        return self.items[index]

    def eq_index(self, key: K) -> int:
        index = self.gteq_index(key)
        if index is None:
            return None
        if self.keys[index] != key:
            return None
        return index

    def lteq_index(self, key: K) -> int:
        index = bisect_right(self.keys, key) - 1
        if index == -1:
            return None
        return index

    def lt_index(self, key: K) -> int:
        index = bisect_left(self.keys, key) - 1
        if index == -1:
            return None
        return index

    def gt_index(self, key: K) -> int:
        index = bisect_right(self.keys, key)
        if index == len(self.keys):
            return None
        return index

    def gteq_index(self, key: K) -> int:
        index = bisect_left(self.keys, key)
        if index == len(self.keys):
            return None
        return index
