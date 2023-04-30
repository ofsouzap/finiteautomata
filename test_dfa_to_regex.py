from DFA import DFA
from conversion import dfa_to_regular_expression, regular_expression_to_nfae
from test_nfae_to_dfa import runner_comparison_test


# N.B. these tests will be converting the regular expression computed back into an NFA-ε but, if the other code works (this is a very important "if"), this is fine to test with


# def test_general_0():
#
#     dfa = DFA(
#         state_count=...,
#         accepting_states={...},
#         alphabet={"a","b"},
#         transitions={
#             (..., ...): ...,
#             ...
#         },
#         initial_state=...
#     )
# 
#     regex = dfa_to_regular_expression(dfa)
#     nfae = regular_expression_to_nfae(regex)
#
#     runner_comparison_test(nfae, dfa, ...)


def test_general_0():

    dfa = DFA(
        state_count=1,
        accepting_states={0},
        alphabet={"a"},
        transitions={
            (0, "a"): 0
        },
        initial_state=0
    )

    regex = dfa_to_regular_expression(dfa)
    nfae = regular_expression_to_nfae(regex)

    runner_comparison_test(nfae, dfa, 3)


def test_general_1():

    dfa = DFA(
        state_count=2,
        accepting_states={0},
        alphabet={"a","b"},
        transitions={
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 0,
        },
        initial_state=0
    )

    regex = dfa_to_regular_expression(dfa)
    nfae = regular_expression_to_nfae(regex)

    runner_comparison_test(nfae, dfa, 6)


def test_general_2():

    dfa = DFA(
        state_count=3,
        accepting_states={2},
        alphabet={"a","b"},
        transitions={
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 2,
            (2, "a"): 1,
            (2, "b"): 2,
        },
        initial_state=0
    )

    regex = dfa_to_regular_expression(dfa)
    nfae = regular_expression_to_nfae(regex)

    runner_comparison_test(nfae, dfa, 6)


def test_general_3():

    dfa = DFA(
        state_count=6,
        accepting_states={5},
        alphabet={"a","b"},
        transitions={
            (0, "a"): 1,
            (0, "b"): 0,
            (1, "a"): 2,
            (1, "b"): 3,
            (2, "a"): 4,
            (2, "b"): 2,
            (3, "a"): 5,
            (3, "b"): 5,
            (4, "a"): 5,
            (4, "b"): 5,
            (5, "a"): 0,
            (5, "b"): 0,
        },
        initial_state=0
    )

    regex = dfa_to_regular_expression(dfa)
    nfae = regular_expression_to_nfae(regex)

    runner_comparison_test(nfae, dfa, 10)
