from typing import Set, Dict, Tuple, Optional
from NFAe import NFAe, State, Symbol
from conversion import merge_nfaes


PolarState = Tuple[State, bool]  # False means from `a`, True means from `b`


def check_result(res: NFAe,
                 a_mapping: Dict[State, State],
                 b_mapping: Dict[State, State],
                 state_count: int,
                 alphabet: Set[Symbol],
                 initial_state: PolarState,
                 acceptings: Set[PolarState],
                 transitions: Dict[Tuple[PolarState, Optional[Symbol]], Set[PolarState]]
                 ) -> None:

    # Basics

    assert res.state_count == state_count
    assert res.alphabet == alphabet
    assert res.initial_state == a_mapping[initial_state[0]] if not initial_state[1] else b_mapping[initial_state[0]]

    # Accepting states

    assert len(res.accepting_states) == len(acceptings)

    for (s, s_ab) in acceptings:

        res_s = a_mapping[s] if not s_ab else b_mapping[s]

        assert res_s in res.accepting_states

    # Transitions

    assert len(res.transitions) == len(transitions)

    for transition in transitions:

        ((s_p, s_ab), sym) = transition

        ts_p = transitions[transition]

        s = a_mapping[s_p] if not s_ab else b_mapping[s_p]
        ts = set([a_mapping[t_p] if not t_ab else b_mapping[t_p] for (t_p, t_ab) in ts_p])

        assert (s, sym) in res.transitions

        assert res.transitions[(s, sym)] == ts


def test_with_single_no_connection():

    a = NFAe(
        state_count=5,
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

    b = NFAe(
        state_count=1,
        accepting_states=set(),
        alphabet={"a", "b"},
        transitions={},
        initial_state=0
    )

    res, a_mapping, b_mapping \
        = merge_nfaes(a, b,
                      {
                      },
                      {
                      },
                      0,
                      False
        )

    check_result(res, a_mapping, b_mapping,
                 a.state_count + b.state_count,
                 a.alphabet,
                 (0, False),
                 {(0, False), (4, False)},
                 {
                    ((0, False), "a"): {(1, False), (3, False)},
                    ((1, False), "a"): {(2, False)},
                    ((2, False), "a"): {(1, False)},
                    ((2, False), "b"): {(3, False), (4, False)},
                    ((2, False), None): {(0, False)},
                    ((3, False), "b"): {(4, False)}
                 })


def test_general_0():

    a = NFAe(
        state_count=5,
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

    b = NFAe(
        state_count=2,
        accepting_states={1},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): {1},
            (1, "a"): {0}
        },
        initial_state=0
    )

    res, a_mapping, b_mapping \
        = merge_nfaes(a, b,
                      {
                        (0, None): {0}
                      },
                      {
                        (1, "b"): {3}
                      },
                      0,
                      True
        )

    check_result(res, a_mapping, b_mapping,
                 a.state_count + b.state_count,
                 a.alphabet,
                 (0, True),
                 {(0, False), (4, False), (1, True)},
                 {
                    ((0, False), "a"): {(1, False), (3, False)},
                    ((1, False), "a"): {(2, False)},
                    ((2, False), "a"): {(1, False)},
                    ((2, False), "b"): {(3, False), (4, False)},
                    ((2, False), None): {(0, False)},
                    ((3, False), "b"): {(4, False)},

                    ((0, True), "a"): {(1, True)},
                    ((1, True), "a"): {(0, True)},

                    ((0, False), None): {(0, True)},
                    ((1, True), "b"): {(3, False)}
                 })
