from __future__ import annotations
from typing import cast


class Coord:
    def __init__(self, x: float, y: float):
        self._xy: list[float] = [x, y]

    @property
    def xy(self) -> tuple[float, float]:
        return cast(tuple[float, float], tuple(self._xy))

    @xy.setter
    def xy(self, value: tuple[float, float]):
        self._xy = list(value)

    @property
    def x(self) -> float:
        return self._xy[0]

    @x.setter
    def x(self, value: float):
        self._xy[0] = value

    @property
    def y(self) -> float:
        return self._xy[1]

    @y.setter
    def y(self, value: float):
        self._xy[1] = value

    def __getitem__(self, key: int) -> float:
        return self._xy[key]

    def __setitem__(self, key: int, value: float):
        self._xy[key] = value

    def __iter__(self):
        return iter(self._xy)

    def __add__(self, other: tuple[float, float]):
        ax, ay = self
        bx, by = other
        return Coord(ax + bx, ay + by)

    __radd__ = __add__

    def __iadd__(self, other: tuple[float, float]):
        self._xy = list(self + other)
        return self

    def __sub__(self, other: tuple[float, float]):
        ax, ay = self
        bx, by = other
        return Coord(ax - bx, ay - by)

    def __rsub__(self, other: tuple[float, float]):
        ax, ay = other
        bx, by = self
        return Coord(ax - bx, ay - by)

    def __isub__(self, other: tuple[float, float]):
        self._xy = list(self - other)
        return self

    def __mul__(self, other: float):
        """Coord(2, 3) * 4 == Coord(8, 12)"""
        x, y = self
        return Coord(x * other, y * other)

    __rmul__ = __mul__

    def __imul__(self, other: float):
        self._xy = list(self * other)
        return self

    def __truediv__(self, other: float):
        return self * (1 / other)

    def __itruediv__(self, other: float):
        self._xy = list(self / other)
        return self

    def __eq__(self, other: tuple[float, float]):
        return (*self,) == (*other,)

    def __str__(self):
        return str(tuple(self._xy))

    def __repr__(self):
        return f"<Coord({self.x}, {self.y})>"

    def __len__(self):
        return 2
