import pytest

from nygame.common import Index


class Item:
    def __init__(self, name, num):
        self.name = name
        self.num = num


@pytest.fixture(autouse=True)
def data():
    global index, items
    items = [
        Item("minus four", -4),
        Item("zero", 0),
        Item("two", 2),
        Item("four", 4),
        Item("five", 5),
        Item("seven", 7)
    ]
    index = Index(items, "num")


def test_getitem_single():
    assert index[-7] is None
    assert index[5].name == "five"
    assert index[5.5] is None
    assert index[9] is None


def test_getitem_range():
    assert index[-7:-5] == []
    assert index[5:] == items[4:]
    assert index[5.5:] == items[5:]
    assert index[:5] == items[:4]
    assert index[:5.5] == items[:5]
    assert index[0:7:2] == items[1:5:2]
    assert index[20:] == []
    assert index[-20:] == items


def test_word_range():
    items = [
        Item("w1", 6049),
        Item("w2", 6144),
        Item("w3", 6264),
        Item("w4", 6384),
        Item("w5", 6516),
        Item("w6", 6624)
    ]
    index = Index(items, "num")
    assert index[:6627 + 1] == items
    assert index[6627 + 1:] == []


def test_eq():
    assert index.eq(-7) is None
    assert index.eq(5).name == "five"
    assert index.eq(5.5) is None
    assert index.eq(9) is None


def test_lteq():
    assert index.lteq(-7) is None
    assert index.lteq(5).name == "five"
    assert index.lteq(5.5).name == "five"
    assert index.lteq(9).name == "seven"


def test_lt():
    assert index.lt(-7) is None
    assert index.lt(5).name == "four"
    assert index.lt(5.5).name == "five"
    assert index.lt(9).name == "seven"


def test_gteq():
    assert index.gteq(-7).name == "minus four"
    assert index.gteq(5).name == "five"
    assert index.gteq(5.5).name == "seven"
    assert index.gteq(9) is None


def test_gt():
    assert index.gt(-7).name == "minus four"
    assert index.gt(5).name == "seven"
    assert index.gt(5.5).name == "seven"
    assert index.gt(9) is None


def test_eq_index():
    assert index.eq_index(-7) is None
    assert index.eq_index(5) == 4
    assert index.eq_index(5.5) is None
    assert index.eq_index(9) is None


def test_lteq_index():
    assert index.lteq_index(-7) is None
    assert index.lteq_index(5) == 4
    assert index.lteq_index(5.5) == 4
    assert index.lteq_index(9) == 5


def test_lt_index():
    assert index.lt_index(-7) is None
    assert index.lt_index(5) == 3
    assert index.lt_index(5.5) == 4
    assert index.lt_index(9) == 5


def test_gteq_index():
    assert index.gteq_index(-7) == 0
    assert index.gteq_index(5) == 4
    assert index.gteq_index(5.5) == 5
    assert index.gteq_index(9) is None


def test_gt_index():
    assert index.gt_index(-7) == 0
    assert index.gt_index(5) == 5
    assert index.gt_index(5.5) == 5
    assert index.gt_index(9) is None
