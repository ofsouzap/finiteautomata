from typing import Set, Tuple, Dict, Optional
from copy import copy

from FiniteAutomaton import State, Symbol, Alphabet


class NFAe:

    Transitions = Dict[Tuple[State, Optional[Symbol]], Set[State]]

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

    def find_epsilon_transitions(self, state: State) -> Set[State]:

        outs: Set[State] = set()

        for (s, sym_opt) in self.transitions:

            if s != state:
                continue
            if sym_opt is not None:
                continue

            assert (s == state) and (sym_opt is None)

            nexts = self.transitions[(s, sym_opt)]

            for t in nexts:
                outs.add(t)

        return outs

    def get_next_states(self, curr_state: State, symbol: Symbol) -> Set[State]:
        """N.B. will only use symbol-requiring transitions, won't use ε-transitions"""

        assert symbol in self.alphabet, "Invalid symbol"

        if (curr_state, symbol) in self.transitions:
            return self.transitions[(curr_state, symbol)]
        else:
            return set()
