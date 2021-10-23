import pytest

from nygame.common import Coord


@pytest.fixture(autouse=True)
def data():
    global x, y, xy, a, b, ab
    x = 1
    y = 2
    xy = (x, y)
    a = 5
    b = 6
    ab = (a, b)


def test_init():
    assert Coord(x, y) == xy
    assert Coord(*xy) == xy


def test_eq():
    assert Coord(*xy) == xy
    assert xy == Coord(*xy)
    assert Coord(*xy) == Coord(*xy)
    assert Coord(*xy) != ab
    assert ab != Coord(*xy)
    assert Coord(*xy) != Coord(*ab)


def test_attr_get():
    c = Coord(*xy)
    assert c.x == x
    assert c.y == y
    assert c.xy == xy


def test_attr_set():
    c = Coord(*xy)
    c.xy = ab
    assert c == ab

    c = Coord(*xy)
    assert c == Coord(*xy)
    c.x = a
    c.y = b
    assert c == ab


def test_index_get():
    assert Coord(*xy)[0] == x
    assert Coord(*xy)[1] == y


def test_len():
    assert len(Coord(*xy)) == 2


def test_index_set():
    c = Coord(*xy)
    c[0] = a
    c[1] = b
    c == ab


def test_iter():
    assert tuple(Coord(*xy)) == xy


def test_add():
    c = Coord(*xy) + (2, 3)
    assert isinstance(c, Coord)
    assert c == (3, 5)
    c = (2, 3) + Coord(*xy)
    assert isinstance(c, Coord)
    assert c == (3, 5)
    c = Coord(*xy)
    c += (2, 3)
    assert isinstance(c, Coord)
    assert c == (3, 5)


def test_sub():
    c = Coord(*xy) - (2, 3)
    assert isinstance(c, Coord)
    assert c == (-1, -1)
    c = (2, 3) - Coord(*xy)
    assert isinstance(c, Coord)
    assert c == (1, 1)
    c = Coord(*xy)
    c -= (2, 3)
    assert isinstance(c, Coord)
    assert c == (-1, -1)


def test_mul():
    c = Coord(*xy) * 4
    assert isinstance(c, Coord)
    assert c == (4, 8)
    c = 4 * Coord(*xy)
    assert isinstance(c, Coord)
    assert c == (4, 8)
    c = Coord(*xy)
    c *= 4
    assert isinstance(c, Coord)
    assert c == (4, 8)


def test_div():
    c = Coord(*xy) / 4
    assert isinstance(c, Coord)
    assert c == (0.25, 0.5)
    c = Coord(*xy)
    c /= 4
    assert isinstance(c, Coord)
    assert c == (0.25, 0.5)


def test_str():
    assert str(Coord(*xy)) == "(1, 2)"
    assert repr(Coord(*xy)) == "<Coord(1, 2)>"
