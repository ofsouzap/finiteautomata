from typing import List, Set, Tuple, Dict

from FiniteAutomaton import State, Symbol, Alphabet


class NFA:

    Transitions = Dict[Tuple[State, Symbol], Set[State]]

    def __init__(self,
                 state_count: State,
                 accepting_states: Set[State],
                 alphabet: Alphabet,
                 transitions: Transitions,
                 initial_state: State):

        self.state_count = state_count
        self.accepting_states = accepting_states
        self.alphabet = alphabet
        self.transitions = transitions

        self.initial_state = initial_state

    def is_valid_state(self, state: State) -> bool:
        return 0 <= state < self.state_count

    def get_next_states(self, curr_state: State, symbol: Symbol) -> Set[State]:

        assert symbol in self.alphabet, "Invalid symbol"

        if (curr_state, symbol) in self.transitions:
            return self.transitions[(curr_state, symbol)]
        else:
            return set()
