from typing import List, Set
from NFA import NFA, State, Symbol
from NFARunner import NFARunner


def runner_test(runner: NFARunner, string: List[Symbol], states: List[Set[State]], acceptings: List[bool]) -> None:

    assert len(string) + 1 == len(states) == len(acceptings), "Differing length test parameters passed"

    assert runner.states == states[0]
    assert runner.accepting == acceptings[0]

    for c, ss, a in zip(string, states[1:], acceptings[1:]):

        runner.read_symbol(c)
        assert runner.states == ss
        assert runner.accepting == a


def test_init_valid():

    nfa = NFA(
        state_count=3,
        accepting_states={1},
        alphabet={"a", "b", "c"},
        transitions={
            (0, "a"): {0},
            (0, "b"): {1},
            (2, "b"): set(),
            (0, "c"): {2, 3},
            (1, "a"): {0, 1}
        },
        initial_state=0
    )


def test_general_0():

    nfa = NFA(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFARunner(nfa)

    runner_test(runner,
                string=["a","a","a","b"],
                states=[
                    {0},
                    {1, 3},
                    {2},
                    {1},
                    set()
                ],
                acceptings=[True, False, False, False, False])


def test_general_1():

    nfa = NFA(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFARunner(nfa)

    runner_test(runner,
                string=["a","a","b","b","b"],
                states=[
                    {0},
                    {1, 3},
                    {2},
                    {3, 4},
                    {4},
                    set()
                ],
                acceptings=[True, False, False, True, True, False])


def test_invalid_symbol():

    nfa = NFA(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFARunner(nfa)

    runner.read_symbol("a")

    try:
        runner.read_symbol("c")
        raise Exception("No exception raised")
    except:
        pass
