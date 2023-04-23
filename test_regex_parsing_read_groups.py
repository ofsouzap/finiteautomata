from RegularExpression import *
from regular_expression_parsing import parse, _read_group, GroupList, _StringStream


def assert_group_list_equal(a: GroupList, b: GroupList) -> None:

    assert len(a) == len(b)

    for xa, xb in zip(a, b):

        match (xa, xb):
            case (str() as sa, str() as sb):
                assert sa == sb
            case (str(), list()) | (list(), str()):
                raise Exception("Encountered str in one GroupList but list in the other")
            case (list() as xsa, list() as xsb):
                assert_group_list_equal(xsa, xsb)


def test_read_group_0():

    inp: str = "abcbc"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a","b","c","b","c"])


def test_read_group_1():

    inp: str = "ab(cb)c"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a","b",["c","b"],"c"])


def test_read_group_2():

    inp: str = "abb*a||b(ab)*"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a","b","b","*","a","|","|","b",["a","b"],"*"])


def test_read_group_3():

    inp: str = "a(ba)*"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a",["b","a"],"*"])


def test_read_group_4():

    inp: str = "(abc|a)*"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, [["a","b","c","|","a"],"*"])


def test_read_group_5():

    inp: str = "aa(ba*(c|a)(a|(ab)))a"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a","a",["b","a","*",["c","|","a"],["a","|",["a","b"]]],"a"])


def test_read_group_6():

    inp: str = "a(ba)"
    out: GroupList = _read_group(_StringStream(inp))

    assert_group_list_equal(out, ["a",["b","a"]])
