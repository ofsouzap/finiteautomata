from typing import Set, Iterator
from conversion import regular_expression_to_nfae
from RegularExpression import *
from FiniteAutomaton import String
from NFAe import NFAe, Symbol
from NFAeRunner import NFAeRunner


def compare_strings(a: String, b: String) -> bool:

    if len(a) != len(b):
        return False

    for xa, xb in zip(a, b):
        if xa != xb:
            return False

    return True


def generate_strings(alphabet: Set[Symbol],
                     prev: String,
                     N: int) -> Iterator[String]:

    yield prev

    if N == 0:

        return

    else:

        for c in alphabet:

            new = prev + c

            for out in generate_strings(alphabet, new, N-1):
                yield out  # Yield with greater lengths


def do_test(regex: RegularExpression,
            alphabet: Set[Symbol],
            N: int,
            exp_accepts: Set[String]) -> None:

    nfae: NFAe = regular_expression_to_nfae(regex)

    assert all(map(lambda s: len(s) <= N, exp_accepts))

    for string in generate_strings(alphabet, String(), N):

        runner = NFAeRunner(nfae)

        for sym in string:
            runner.read_symbol(sym)

        if any(map(lambda s: compare_strings(string, s), exp_accepts)):
            assert runner.accepting, "Should accept \"" + "".join(string) + "\" but doesn't"
        else:
            assert not runner.accepting, "Shouldn't accept \"" + "".join(string) + "\" but does"


def test_null():

    regex: RegularExpression = RegularExpression({"a", "b", "c"}, RENull())

    do_test(
        regex,
        {"a", "b", "c"},
        3,
        set()
    )


def test_empty():

    regex: RegularExpression = RegularExpression({"a", "b", "c"}, REEmpty())

    do_test(
        regex,
        {"a", "b", "c"},
        3,
        {String()}
    )


def test_single():

    regex = RegularExpression({"a", "b", "c"}, RESym("a"))

    do_test(
        regex,
        {"a", "b", "c"},
        3,
        {String("a")}
    )


def test_conc_0():

    regex = RegularExpression({"a", "b", "c"}, REConc(RESym("a"), RESym("b"), RESym("b"), RESym("a")))

    do_test(
        regex,
        {"a", "b", "c"},
        5,
        {String("a", "b", "b", "a")}
    )


def test_repeat():

    regex = RegularExpression(
        {"a", "b", "c"},
        RERepeat(re_lit_string("aba"))
    )

    do_test(
        regex,
        {"a", "b", "c"},
        6,
        {
            String(),
            String("a","b","a"),
            String("a","b","a","a","b","a"),
        }
    )


def test_union():

    regex = RegularExpression(
        {"a", "b", "c"},
        REUnion(
            re_lit_string("aaabc"),
            RERepeat(re_lit_string("ac")),
            RERepeat(re_lit_string("bb")),
            RENull()
        )
    )

    do_test(
        regex,
        {"a", "b", "c"},
        6,
        {

            String("a","a","a","b","c"),

            String(),
            String("a","c"),
            String("a","c","a","c"),
            String("a","c","a","c","a","c"),

            String("b", "b"),
            String("b", "b", "b", "b"),
            String("b", "b", "b", "b", "b", "b")

        }
    )


def test_conc_1():

    regex = RegularExpression({"a", "b", "c"}, REConc(
        RESym("a"),
        RERepeat(RESym("b")),
        RESym("a")
    ))

    do_test(
        regex,
        {"a", "b", "c"},
        5,
        {
            String("a", "a"),
            String("a", "b", "a"),
            String("a", "b", "b", "a"),
            String("a", "b", "b", "b", "a"),
        }
    )


def test_conc_2():

    regex = RegularExpression({"a", "b", "c"}, REConc(
        RESym("a"),
        RERepeat(RESym("a")),
        REEmpty()
    ))

    do_test(
        regex,
        {"a", "b"},
        3,
        {
            String("a"),
            String("a","a"),
            String("a","a","a"),
        }
    )


def test_general_0():

    # Using the expression: ab(a*)|c∅|a(a*)(b*)|ε

    regex = RegularExpression({"a","b","c"}, REUnion(
        REConc(re_lit_string("ab"), RERepeat(RESym("a"))),
        REConc(RESym("c"), RENull()),
        REConc(RESym("a"), RERepeat(RESym("a")), RERepeat(RESym("b"))),
        REEmpty()
    ))

    do_test(
        regex,
        {"a", "b", "c"},
        5,
        {

            String(),

            String("a","b"),
            String("a","b","a"),
            String("a","b","a","a"),
            String("a","b","a","a","a"),

            String("a"),
            String("a","a"),
            String("a","a","a"),
            String("a","a","b"),
            String("a","a","b"),
            String("a","b","b"),
            String("a","a","a","a"),
            String("a","a","a","b"),
            String("a","a","b","b"),
            String("a","b","b","b"),
            String("a","a","a","a","a"),
            String("a","a","a","a","b"),
            String("a","a","a","b","b"),
            String("a","a","b","b","b"),
            String("a","b","b","b","b"),

        }
    )
