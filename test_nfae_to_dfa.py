from typing import Iterator
from conversion import nfae_to_dfa
from _nfae_to_dfa import _gen_epsilon_mapping
from FiniteAutomaton import Alphabet, Symbol, String
from NFAe import NFAe
from DFA import DFA
from NFAeRunner import NFAeRunner
from DFARunner import DFARunner


def test_epsilon_mapping_0():

    nfae: NFAe = NFAe(
        state_count=5,
        accepting_states={3, 4},
        alphabet={"a","b"},
        transitions={
            (0, None): {1, 2},
            (0, "b"): {3},
            (1, None): {2},
            (2, None): {4},
            (2, "b"): {4},
            (3, None): {4},
            (3, "a"): {2},
            (4, "b"): {2}
        },
        initial_state=0
    )

    e_mapping = _gen_epsilon_mapping(nfae)

    assert e_mapping[0] == {0,1,2,4}
    assert e_mapping[1] == {1,2,4}
    assert e_mapping[2] == {2,4}
    assert e_mapping[3] == {3,4}
    assert e_mapping[4] == {4}


def iter_possible_strings(alphabet: Alphabet, N: int, acc: String) -> Iterator[String]:

    if N == 0:

        yield acc

    else:

        for sym in alphabet:
            for out in iter_possible_strings(alphabet, N-1, acc + sym):
                yield out


def assert_runners_equal(runner_n: NFAeRunner, runner_d: DFARunner) -> None:

    assert runner_n.accepting == runner_d.accepting


def runner_comparison_test(nfae: NFAe, N: int) -> None:

    for string in iter_possible_strings(nfae.alphabet, N, String()):

        runner_n = NFAeRunner(nfae)

        dfa = nfae_to_dfa(nfae)
        runner_d = DFARunner(dfa)

        assert_runners_equal(runner_n, runner_d)

        for sym in string:

            runner_n.read_symbol(sym)
            runner_d.read_symbol(sym)

            assert_runners_equal(runner_n, runner_d)


def test_general_0():

    nfae: NFAe = NFAe(
        state_count=4,
        accepting_states={3},
        alphabet={"a","b","c"},
        transitions={
            (0, "a"): {1, 2},
            (1, "a"): {3},
            (1, "c"): {1},
            (2, "b"): {3}
        },
        initial_state=0
    )

    runner_comparison_test(nfae, 5)


def test_general_1():

    nfae: NFAe = NFAe(
        state_count=4,
        accepting_states={3},
        alphabet={"a","b","c"},
        transitions={
            (0, None): {1},
            (0, "a"): {1, 2},
            (1, "a"): {3},
            (1, "b"): {1},
            (1, "c"): {0, 1, 2, 3},
            (2, "b"): {3},
            (3, None): {0, 2}
        },
        initial_state=0
    )

    runner_comparison_test(nfae, 10)
