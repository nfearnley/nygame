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
