from RegularExpression import *


def test_0():

    # a*b|bb|∅

    regex = REUnion(
        REConc(RERepeat(RESym("a")), RESym("b")),
        REConc(RESym("b"), RESym("b")),
        RENull()
    )

    assert str(regex) == "(((a)*)(b))|((b)(b))|(∅)"
