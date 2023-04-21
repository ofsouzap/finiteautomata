from DFA import DFA
from DFARunner import DFARunner


def test_init_valid():

    dfa = DFA(
        state_count=3,
        accepting_states={1},
        alphabet={"a", "b", "c"},
        transitions={
            (0, "a"): 0,
            (0, "b"): 1,
            (0, "c"): 2,
            (1, "a"): 0,
            (1, "b"): 1,
            (1, "c"): 2,
            (2, "a"): 0,
            (2, "b"): 1,
            (2, "c"): 2,
        },
        initial_state=0
    )


def test_init_invalid():

    try:

        dfa = DFA(
            state_count=3,
            accepting_states={1},
            alphabet={"a", "b", "c"},
            transitions={
                (0, "a"): 0,
                (0, "b"): 1,
                (1, "a"): 0,
                (1, "b"): 1,
                (1, "c"): 2,
                (2, "a"): 0,
                (2, "b"): 1,
                (2, "c"): 2,
            },
            initial_state=0
        )

        raise Exception("DFA creation didn't raise error")

    except:

        pass


def test_general_0():

    dfa = DFA(
        state_count=3,
        accepting_states={2},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): 0,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 2,
            (2, "a"): 1,
            (2, "b"): 0,
        },
        initial_state=1
    )

    runner = DFARunner(dfa)

    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("b")
    assert runner.state == 2
    assert runner.accepting
    runner.read_symbol("a")
    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("b")
    assert runner.state == 2
    assert runner.accepting
    runner.read_symbol("b")
    assert runner.state == 0
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 0
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 0
    assert not runner.accepting
    runner.read_symbol("b")
    assert runner.state == 0
    assert not runner.accepting


def test_invalid_symbol():

    dfa = DFA(
        state_count=3,
        accepting_states={2},
        alphabet={"a", "b"},
        transitions={
            (0, "a"): 0,
            (0, "b"): 0,
            (1, "a"): 1,
            (1, "b"): 2,
            (2, "a"): 1,
            (2, "b"): 0,
        },
        initial_state=1
    )

    runner = DFARunner(dfa)

    assert runner.state == 1
    assert not runner.accepting
    runner.read_symbol("a")
    assert runner.state == 1
    assert not runner.accepting

    try:
        runner.read_symbol("c")
        raise Exception("No exception raised")
    except:
        pass
