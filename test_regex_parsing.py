from RegularExpression import *
from regular_expression_parsing import parse

from test_regex_to_nfae import do_test as check_regex_acceptance


def test_general_0():

    regex: RegularExpression = parse("abb*a||b(ab)*")
    check_regex_acceptance(
        regex=regex,
        alphabet={"a","b"},
        N=5,
        exp_accepts={
            String("a","b","a"),
            String("a","b","b","a"),
            String("a","b","b","b","a"),
            String(),
            String("b"),
            String("b","a","b"),
            String("b","a","b","a","b"),
        }
    )


def test_general_1():

    regex: RegularExpression = parse("a(ba)*")
    check_regex_acceptance(
        regex=regex,
        alphabet={"a","b"},
        N=6,
        exp_accepts={
            String("a"),
            String("a","b","a"),
            String("a","b","a","b","a"),
        }
    )


def test_general_2():

    regex: RegularExpression = parse("(abc|a)*")
    check_regex_acceptance(
        regex=regex,
        alphabet={"a","b"},
        N=4,
        exp_accepts={
            String(),
            String("a","b","c"),
            String("a","b","c","a"),
            String("a"),
            String("a","a","b","c"),
            String("a","a"),
            String("a","a","a"),
            String("a","a","a","a"),
        }
    )


def test_general_3():

    regex: RegularExpression = parse("aa(ba*(c|a)(a|(ab)))a")
    check_regex_acceptance(
        regex=regex,
        alphabet={"a","b"},
        N=10,
        exp_accepts={

            String("a","a","b","c","a","a"),
            String("a","a","b","a","c","a","a"),
            String("a","a","b","a","a","c","a","a"),
            String("a","a","b","a","a","a","c","a","a"),
            String("a","a","b","a","a","a","a","c","a","a"),

            String("a","a","b","c","a","b","a"),
            String("a","a","b","a","c","a","b","a"),
            String("a","a","b","a","a","c","a","b","a"),
            String("a","a","b","a","a","a","c","a","b","a"),

            String("a","a","b","a","a","a"),
            String("a","a","b","a","a","a","a"),
            String("a","a","b","a","a","a","a","a"),
            String("a","a","b","a","a","a","a","a","a"),
            String("a","a","b","a","a","a","a","a","a","a"),

            String("a","a","b","a","a","b","a"),
            String("a","a","b","a","a","a","b","a"),
            String("a","a","b","a","a","a","a","b","a"),
            String("a","a","b","a","a","a","a","a","b","a"),

        }
    )
