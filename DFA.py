from typing import List, Set, Tuple, Dict

from FiniteAutomaton import State, Symbol, Alphabet


class DFA:

    Transitions = Dict[Tuple[State, Symbol], State]

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

        assert self.__check_is_deterministic()

    def __check_is_deterministic(self) -> bool:

        for s in range(0, self.state_count):
            for c in self.alphabet:
                if (s, c) not in self.transitions:
                    return False

        return True

    def is_valid_state(self, state: State) -> bool:
        return 0 <= state < self.state_count

    def get_next_state(self, curr_state: State, symbol: Symbol) -> State:

        assert symbol in self.alphabet, "Invalid symbol"

        return self.transitions[(curr_state, symbol)]
