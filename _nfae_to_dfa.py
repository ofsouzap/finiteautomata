from typing import Dict, Set, Iterator, Union
from FiniteAutomaton import State, Symbol
from NFAe import NFAe
from DFA import DFA
from _mathutil import ipow


class SubsetMapping:

    def __init__(self, nfae: NFAe):

        # The number of states in the NFAe
        self.__n = nfae.state_count

    def nfae_to_dfa(self, subset: Set[State]) -> State:

        n: int = 0

        for i in subset:

            n += 1 << i

        return n

    def dfa_to_nfae(self, state: State) -> Set[State]:

        subset: Set[State] = set()

        for i in range(self.__n):

            if __bitsel(state, i):
                subset.add(i)

        return subset

    def __getitem__(self, key: Set[State]) -> State:

        return self.nfae_to_dfa(key)


def __bitsel(n: int, i: int) -> bool:
    return (n >> i) & 1 != 0


def __n_to_subset(n: int, bit_count: int) -> Set[State]:

    subset: Set[State] = set()

    for i in range(bit_count):
        if __bitsel(n, i):
            subset.add(i)

    return subset


def __it_subset_selectors(n: int) -> Iterator[int]:
    for i in range(n):
        yield ipow(2, i)


def _gen_epsilon_mapping(nfae: NFAe) -> Dict[State, Set[State]]:

    mapping: Dict[State, Set[State]] = {}

    for start in range(nfae.state_count):

        ends = [start]
        i = 0

        while i < len(ends):

            s = ends[i]
            i += 1

            key = (s, None)

            if key not in nfae.transitions:
                continue

            for t in nfae.transitions[(s, None)]:
                if t not in ends:
                    ends.append(t)

        mapping[start] = set(ends)

    return mapping


def __possible_next_states(nfae: NFAe, e_mapping: Dict[State, Set[State]], subset: Set[State], sym: Symbol) -> Set[State]:

    next_states: Set[State] = set()

    # Find direct next states

    for s in subset:

        key_n = (s, sym)

        if key_n in nfae.transitions:
            ts_n = nfae.transitions[key_n]
        else:
            ts_n: Set[State] = set()

        next_states |= ts_n

    # Add epsilon-transition results

    e_states: Set[State] = set()

    for s in next_states:
        e_states |= e_mapping[s]

    next_states |= e_states  # Add found states to results

    # Return results

    return next_states


def __gen_transitions(nfae: NFAe, e_mapping: Dict[State, Set[State]], mapping: SubsetMapping) -> DFA.Transitions:

    dfa_transitions: DFA.Transitions = {}

    for n in range(ipow(2, nfae.state_count)):

        subset_n: Set[State] = __n_to_subset(n, nfae.state_count)

        for sym in nfae.alphabet:

            key_d = (mapping[subset_n], sym)

            # Find the possible next states from any of the states in `subset_n`` using symbol `sym`

            next_states_n: Set[State] = __possible_next_states(nfae, e_mapping, subset_n, sym)

            # Determine next state in dfa from next states

            next_state_d = mapping[next_states_n]

            # Add transition to transitions

            dfa_transitions[key_d] = next_state_d

    # Return transitions

    return dfa_transitions


def __gen_accepting_states(nfae: NFAe, mapping: SubsetMapping) -> Set[State]:

    dfa_accepting_states: Set[State] = set()

    for n in range(ipow(2, nfae.state_count)):

        subset_n: Set[State] = __n_to_subset(n, nfae.state_count)

        # If any of the states in subset_n are accepting states then add the subset to the DFA accepting states
        if len(nfae.accepting_states & subset_n) > 0:
            dfa_accepting_states.add(mapping[subset_n])

    return dfa_accepting_states


def convert(nfae: NFAe) -> DFA:

    # Find epsilon-mapping

    e_mapping = _gen_epsilon_mapping(nfae)

    # Create subset-state mapping

    mapping = SubsetMapping(nfae)

    # Set initial state

    initial_nfae_states = e_mapping[nfae.initial_state] | {nfae.initial_state}

    dfa_initial_state: State = mapping[initial_nfae_states]

    # Find new transitions

    dfa_transitions = __gen_transitions(nfae, e_mapping, mapping)

    # Find DFA accepting states

    dfa_accepting_states = __gen_accepting_states(nfae, mapping)

    # Create and return created DFA

    dfa = DFA(
        state_count=ipow(2, nfae.state_count),
        accepting_states=dfa_accepting_states,
        alphabet=nfae.alphabet,
        transitions=dfa_transitions,
        initial_state=dfa_initial_state
    )

    return dfa
