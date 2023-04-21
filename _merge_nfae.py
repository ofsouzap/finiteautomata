from typing import Dict, Tuple, Optional, Set
from NFAe import NFAe, Symbol, State


MergeTransitions = Dict[Tuple[State, Optional[Symbol]], Set[State]]


def merge(a: NFAe,
          b: NFAe,
          a_to_b: MergeTransitions,
          b_to_a: MergeTransitions,
          new_initial_state: State,
          new_initial_state_from_b: bool) -> Tuple[NFAe, Dict[State, State], Dict[State, State]]:
    """Merges two NFA-ε automata with the same alphabets given some new transitions to connect them

Parameters:

    a: `NFAe` - the first automaton to merge

    b: `NFAe` - the second automaton to merge

    a_to_b: `Dict[(AState, Symbol?) -> Set[BState])]` - some transitions to create where \
        the keys are the state in `a` to start the transition from and the symbol that uses the transition (or `None` for an ε-transition) and \
        the values are the set of states in `b` to transition to

    b_to_a: `Dict[(BState, Symbol?) -> Set[State])]` - similar to `a_to_b` but this time the transitions go from `b` and into `a`

    new_initial_state: `State` - the state that should be used as the initial state in the new automaton

    new_initial_state_from_b: `bool` - whether the new initial state specified is the state from `b`. If not then it is assumed to be the one from `a`

Returns:

    out: `NFAe` - the NFA-ε result from the merge

    a_mapping: `Dict[AState -> OutState]` - mapping from states in `a` to states in `out`

    b_mapping: `Dict[BState -> OutState]` - mapping from states in `b` to states in `out`

"""

    aN = a.state_count
    bN = b.state_count
    outN = aN + bN

    # Create state mappings

    b_offset = aN  # State numbers from b are offset by this amount when converted into their

    a_mapping: Dict[State, State] = {}
    for s in range(aN):
        a_mapping[s] = s

    b_mapping: Dict[State, State] = {}
    for s in range(bN):
        b_mapping[s] = s + b_offset

    # Alphabet

    out_alphabet = a.alphabet | b.alphabet

    # Accepting states

    out_accepting_states: Set[State] = set()

    for accA in a.accepting_states:
        out_accepting_states.add(a_mapping[accA])

    for accB in b.accepting_states:
        out_accepting_states.add(b_mapping[accB])

    # Existing transitions

    out_transitions: NFAe.Transitions = {}

    for (s, sym_opt) in a.transitions:

        ts = a.transitions[(s, sym_opt)]

        out_s = a_mapping[s]
        out_ts: Set[State] = set([a_mapping[t] for t in ts])

        assert (out_s, sym_opt) not in out_transitions

        out_transitions[(out_s, sym_opt)] = out_ts

    for (s, sym_opt) in b.transitions:

        ts = b.transitions[(s, sym_opt)]

        out_s = b_mapping[s]
        out_ts: Set[State] = set([b_mapping[t] for t in ts])

        assert (out_s, sym_opt) not in out_transitions

        out_transitions[(out_s, sym_opt)] = out_ts

    # New transitions

    for (s, sym_opt) in a_to_b:

        ts = a_to_b[(s, sym_opt)]

        out_s = a_mapping[s]
        out_ts: Set[State] = set([b_mapping[t] for t in ts])

        key = (out_s, sym_opt)

        if key in out_transitions:

            out_transitions[key] |= out_ts

        else:

            out_transitions[key] = out_ts

    for (s, sym_opt) in b_to_a:

        ts = b_to_a[(s, sym_opt)]

        out_s = b_mapping[s]
        out_ts: Set[State] = set([a_mapping[t] for t in ts])

        key = (out_s, sym_opt)

        if key in out_transitions:

            out_transitions[key] |= out_ts

        else:

            out_transitions[key] = out_ts

    # Initial state

    if new_initial_state_from_b:
        out_initial_state = b_mapping[new_initial_state]
    else:
        out_initial_state = a_mapping[new_initial_state]

    # Generate and return output

    out = NFAe(
        state_count=outN,
        accepting_states=out_accepting_states,
        alphabet=out_alphabet,
        transitions=out_transitions,
        initial_state=out_initial_state
    )

    return out, a_mapping, b_mapping
