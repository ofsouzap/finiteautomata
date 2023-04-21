from typing import List, Set
from NFAe import NFAe, State, Symbol
from NFAeRunner import NFAeRunner


def runner_test(runner: NFAeRunner, string: List[Symbol], states: List[Set[State]], acceptings: List[bool]) -> None:

    assert len(string) + 1 == len(states) == len(acceptings), "Differing length test parameters passed"

    assert runner.states == states[0]
    assert runner.accepting == acceptings[0]

    for c, ss, a in zip(string, states[1:], acceptings[1:]):

        runner.read_symbol(c)
        assert runner.states == ss
        assert runner.accepting == a


def test_init_valid():

    nfae = NFAe(
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

    nfae = NFAe(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (2, None): {0},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFAeRunner(nfae)

    runner_test(runner,
                string=["a","a","a","b"],
                states=[
                    {0},
                    {1, 3},
                    {0, 2},
                    {1, 3},
                    {4}
                ],
                acceptings=[True, False, True, False, True])


def test_general_1():

    nfae = NFAe(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (2, None): {0},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFAeRunner(nfae)

    runner_test(runner,
                string=["a","a","b","b","b"],
                states=[
                    {0},
                    {1, 3},
                    {0, 2},
                    {3, 4},
                    {4},
                    set()
                ],
                acceptings=[True, False, True, True, True, False])


def test_invalid_symbol():

    nfae = NFAe(
        state_count=4,
        accepting_states={0, 4},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1, 3},
            (1, "a"): {2},
            (2, "a"): {1},
            (2, "b"): {3, 4},
            (2, None): {0},
            (3, "b"): {4}
        },
        initial_state=0
    )

    runner = NFAeRunner(nfae)

    runner.read_symbol("a")

    try:
        runner.read_symbol("c")
        raise Exception("No exception raised")
    except:
        pass


def test_multi_e_transition():

    nfae = NFAe(
        state_count=5,
        accepting_states={2},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1},
            (1, None): {3},
            (1, "b"): {2},
            (3, None): {4},
            (4, "a"): {2}
        },
        initial_state=0
    )

    runner = NFAeRunner(nfae)

    runner_test(runner,
                string=["a","b"],
                states=[
                    {0},
                    {1, 3, 4},
                    {2},
                ],
                acceptings=[False, False, True])
